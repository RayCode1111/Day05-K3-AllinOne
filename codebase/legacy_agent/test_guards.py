"""Kiểm 4 guard bằng output LLM giả lập — chạy được không cần API key.

Guard là chỗ đỡ điều kiện cứng "0 case bịa" của quality bar, nên nó phải có
test riêng: nếu guard hỏng thì con số trong eval/ mất ý nghĩa.

    python codebase/test_guards.py
"""

from __future__ import annotations

import corpus
from triage import ap_guard

TIN = corpus.tin_theo_id()


def _chay(item: dict):
    ket_luan = ap_guard(TIN, [item])
    return ket_luan[0] if ket_luan else None


def test_ga_id_bia_bi_bo():
    """G-A — LLM trả về một tin không hề tồn tại trong corpus."""
    assert _chay({"id": "M999", "muc": "NGAY", "vi_sao": "bịa"}) is None


def test_gb_trich_dan_khong_khop():
    """G-B — trích dẫn không có trong tin gốc thì không được tin."""
    kl = _chay(
        {
            "id": "M16",  # TA nhắc hạn nộp spec
            "muc": "NGAY",
            "han_chot": "2026-07-30T23:59:00+07:00",
            "trich_dan": "hạn nộp đã được dời sang 02/08",  # không hề có trong tin
            "do_chac": "cao",
            "vi_sao": "…",
        }
    )
    assert "trich_dan_khong_khop" in kl.co
    assert kl.trich_dan is None
    assert kl.do_chac == "thap"
    assert kl.muc == "GHI_NHO", "phải bị hạ cấp, không được giữ mức NGAY"
    assert kl.viec_can_lam is None, "việc cần làm dựng trên trích dẫn bịa phải bị gỡ"


def test_gb_trich_dan_dung_thi_giu_nguyen():
    """Guard không được phá case đúng — trích dẫn thật thì mức giữ nguyên."""
    kl = _chay(
        {
            "id": "M16",
            "muc": "HOM_NAY",
            "han_chot": "2026-07-30T23:59:00+07:00",
            "trich_dan": "hạn nộp spec.md của Mini Hackathon là 23:59 hôm nay 30/07",
            "do_chac": "cao",
            "vi_sao": "…",
        }
    )
    assert kl.co == []
    assert kl.muc == "HOM_NAY"
    assert kl.han_chot is not None


def test_gc_han_chot_khong_can_cu_bi_xoa():
    """G-C — có hạn chót mà không có trích dẫn đỡ thì xoá hạn chót."""
    kl = _chay(
        {
            "id": "M22",  # GV bổ sung tài liệu, không nói hạn nào
            "muc": "GHI_NHO",
            "han_chot": "2026-08-01T23:59:00+07:00",
            "trich_dan": None,
            "do_chac": "cao",
            "vi_sao": "…",
        }
    )
    assert "han_chot_khong_can_cu" in kl.co
    assert kl.han_chot is None
    assert kl.do_chac == "thap"


def test_gd_tin_don_hoc_vien_khong_thanh_lich():
    """G-D — tin đồn của học viên không bao giờ được lên mức khẩn."""
    kl = _chay(
        {
            "id": "M19",  # "hình như deadline spec được dời sang mai"
            "muc": "NGAY",
            "viec_can_lam": "Yên tâm, deadline đã dời sang mai.",
            "han_chot": "2026-07-31T23:59:00+07:00",
            "trich_dan": "hình như deadline spec được dời sang mai",
            "do_chac": "cao",
            "vi_sao": "…",
        }
    )
    assert "nguon_khong_chinh_thuc" in kl.co
    assert kl.muc == "GHI_NHO"
    assert kl.han_chot is None, "tin đồn không được đặt hạn chót"
    assert kl.hoi_ta, "phải có đường lui: hỏi TA xác nhận"
    assert "Yên tâm" not in (kl.viec_can_lam or ""), (
        "câu trấn an dựng trên tin đồn phải bị thay — đây là lỗi nguy hiểm nhất "
        "vì nó khiến học viên chủ quan rồi nộp muộn"
    )


def test_gd_nguon_chinh_thuc_van_len_duoc_muc_ngay():
    """Guard nguồn không được chặn nhầm GV/TA/Admin."""
    kl = _chay(
        {
            "id": "M36",  # GV đính chính giờ học
            "muc": "NGAY",
            "trich_dan": "buổi chiều bắt đầu lúc 14:00",
            "do_chac": "cao",
            "vi_sao": "…",
        }
    )
    assert kl.co == []
    assert kl.muc == "NGAY"


def test_muc_la_bi_ha_bo_qua():
    kl = _chay({"id": "M01", "muc": "SIÊU_KHẨN", "do_chac": "cao", "vi_sao": "…"})
    assert kl.muc == "BO_QUA"
    assert "muc_khong_hop_le" in kl.co


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ✅ {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} guard test đạt.")
