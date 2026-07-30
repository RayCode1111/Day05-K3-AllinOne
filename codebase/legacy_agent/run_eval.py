"""Chạy trọn bộ golden set và xuất bảng kết quả vào eval/.

Nguyên tắc (02-guide.md §4.1): mỗi lượt chạy TRỌN BỘ, ghi đủ mọi case kể cả
case fail, đối chiếu quality bar đã chốt. Không sửa bar khi thấy kết quả thấp.

    python codebase/run_eval.py            # chạy và ghi eval/run-NN.md
    python codebase/run_eval.py --ghi-chu "sau khi siết luật 4 trong prompt v3"
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

import corpus
from triage import KetLuan, phan_loai_ngay

EVAL_DIR = Path(__file__).resolve().parent.parent / "eval"
GOLDEN = EVAL_DIR / "golden-set.csv"

# Ngày tham chiếu của từng corpus — cố định để các lượt đo so sánh được với nhau.
NGAY_THAM_CHIEU = {"ngay-thuong": "2026-07-30", "tin-hiem": "2026-07-31"}

# Quality bar — CHỐT trong spec.md trước 23:59 N1, không đổi sau đó.
BAR_DUNG_MUC = 0.80
CO_BIA = {"trich_dan_khong_khop", "han_chot_khong_can_cu"}


def nap_golden() -> list[dict]:
    with GOLDEN.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cham(case: dict, kl: KetLuan | None) -> dict:
    """Ba chiều chất lượng — định nghĩa đầy đủ trong eval/rubric-cham.md."""
    if kl is None:
        return {
            "dung_muc": False,
            "can_cu": False,
            "duong_lui": False,
            "muc_thuc": "(THIẾU)",
            "ghi_chu": "agent không trả kết luận cho tin này",
        }

    dung_muc = kl.muc == case["muc_vang"]

    # Chiều 2 — căn cứ truy vết được: không có cờ bịa, và có hạn chót thì phải
    # có trích dẫn nguyên văn đỡ bên dưới.
    co_bia = bool(CO_BIA & set(kl.co))
    han_dung_ky_vong = (case["co_han_chot"] == "co") == bool(kl.han_chot)
    can_cu = (not co_bia) and (kl.han_chot is None or kl.trich_dan is not None)

    # Chiều 3 — đường lui: case đòi hỏi TA thì phải có câu hỏi gửi TA
    duong_lui = bool(kl.hoi_ta) if case["phai_hoi_ta"] == "co" else True

    ghi_chu = []
    if not dung_muc:
        ghi_chu.append(f"đoán {kl.muc}, vàng {case['muc_vang']}")
    if co_bia:
        ghi_chu.append("BỊA: " + ", ".join(sorted(CO_BIA & set(kl.co))))
    if not han_dung_ky_vong:
        ghi_chu.append("hạn chót lệch kỳ vọng")
    if not duong_lui:
        ghi_chu.append("thiếu câu hỏi gửi TA")
    if kl.co and not co_bia:
        ghi_chu.append("guard: " + ", ".join(kl.co))

    return {
        "dung_muc": dung_muc,
        "can_cu": can_cu,
        "duong_lui": duong_lui,
        "muc_thuc": kl.muc,
        "ghi_chu": "; ".join(ghi_chu) or "—",
    }


def so_luot_tiep_theo() -> int:
    return len(list(EVAL_DIR.glob("run-*.md"))) + 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ghi-chu", default="", help="Lượt này khác lượt trước ở chỗ nào")
    args = parser.parse_args()

    cases = nap_golden()
    tat_ca_tin = corpus.tin_theo_id()

    ket_luan: dict[str, KetLuan] = {}
    meta_cac_lo = []
    for ten_corpus in sorted({c["corpus"] for c in cases}):
        messages, _ = corpus.nap(ten_corpus)
        print(f"→ Gọi AI cho corpus '{ten_corpus}' ({len(messages)} tin)…")
        ds, meta = phan_loai_ngay(messages, NGAY_THAM_CHIEU[ten_corpus], ten_lo=ten_corpus)
        meta_cac_lo.append(meta)
        for kl in ds:
            ket_luan[kl.id] = kl

    ket_qua = [(c, cham(c, ket_luan.get(c["msg_id"]))) for c in cases]
    tong = len(ket_qua)
    dung_muc = sum(1 for _, r in ket_qua if r["dung_muc"])
    can_cu = sum(1 for _, r in ket_qua if r["can_cu"])
    duong_lui = sum(1 for _, r in ket_qua if r["duong_lui"])

    # Điều kiện cứng 1 — không được bỏ sót tin mức NGAY
    case_ngay = [(c, r) for c, r in ket_qua if c["muc_vang"] == "NGAY"]
    bo_sot = [c["case_id"] for c, r in case_ngay if not r["dung_muc"]]
    recall_ngay = (len(case_ngay) - len(bo_sot)) / len(case_ngay) if case_ngay else 1.0

    # Điều kiện cứng 2 — không được bịa căn cứ
    so_bia = sum(1 for _, r in ket_qua if "BỊA" in r["ghi_chu"])

    dat_bar = dung_muc / tong >= BAR_DUNG_MUC and recall_ngay == 1.0 and so_bia == 0

    luot = so_luot_tiep_theo()
    path = EVAL_DIR / f"run-{luot:02d}.md"
    dong: list[str] = [
        f"# Lượt đo {luot:02d} — {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"- Prompt: `codebase/prompts/triage.md` version **{meta_cac_lo[0]['prompt_version']}**",
        f"- Model: `{meta_cac_lo[0]['model']}` · temperature 0",
        f"- Số lời gọi AI: {len(meta_cac_lo)} (mỗi corpus 1 lượt, trace trong `codebase/logs/trace.jsonl`)",
        f"- Ghi chú lượt này: {args.ghi_chu or '—'}",
        "",
        "## Đối chiếu quality bar (chốt 23:59 30/07, không đổi)",
        "",
        "| Điều kiện | Bar | Đo được | Đạt? |",
        "|---|---|---|---|",
        f"| Đúng mức | ≥80% | **{dung_muc}/{tong} = {dung_muc/tong*100:.1f}%** | {'✅' if dung_muc/tong >= BAR_DUNG_MUC else '❌'} |",
        f"| Recall mức NGAY (không bỏ sót) | 100% | **{recall_ngay*100:.0f}%** ({len(case_ngay)-len(bo_sot)}/{len(case_ngay)}) | {'✅' if recall_ngay == 1.0 else '❌ bỏ sót: ' + ', '.join(bo_sot)} |",
        f"| Case bịa căn cứ | 0 | **{so_bia}** | {'✅' if so_bia == 0 else '❌'} |",
        "",
        f"**Kết luận lượt này: {'ĐẠT quality bar' if dat_bar else 'CHƯA ĐẠT quality bar'}**",
        "",
        "Chiều phụ trợ: căn cứ truy vết được "
        f"{can_cu}/{tong} ({can_cu/tong*100:.1f}%) · đường lui đúng "
        f"{duong_lui}/{tong} ({duong_lui/tong*100:.1f}%).",
        "",
        "## Toàn bộ case (kể cả case chưa đạt)",
        "",
        "| Case | Tin | Lớp | Loại | Mức vàng | Mức agent | Đúng mức | Căn cứ | Đường lui | Ghi chú |",
        "|---|---|---|---|---|---|:--:|:--:|:--:|---|",
    ]
    tick = {True: "✅", False: "❌"}
    for c, r in ket_qua:
        dong.append(
            f"| {c['case_id']} | `{c['msg_id']}` | {c['lop_kho']} | {c['loai']} | "
            f"{c['muc_vang']} | {r['muc_thuc']} | {tick[r['dung_muc']]} | "
            f"{tick[r['can_cu']]} | {tick[r['duong_lui']]} | {r['ghi_chu']} |"
        )

    fail = [(c, r) for c, r in ket_qua if not r["dung_muc"]]
    dong += ["", "## Phân tích case chưa đạt", ""]
    if not fail:
        dong.append("Không có case sai mức trong lượt này.")
    else:
        theo_lop = Counter(c["lop_kho"] for c, _ in fail)
        dong.append(f"Tổng {len(fail)} case sai mức, phân bố theo lớp: "
                    + ", ".join(f"{k} × {v}" for k, v in theo_lop.most_common()))
        dong.append("")
        for c, r in fail:
            dong.append(
                f"- **{c['case_id']}** (`{c['msg_id']}`, lớp {c['lop_kho']}) — "
                f"{c['mo_ta_tinh_huong']}. Vàng `{c['muc_vang']}`, agent trả `{r['muc_thuc']}`. "
                f"Nhãn vàng đặt vậy vì: {c['vi_sao_nhan_nhu_vay'].lower()}."
            )
        dong += ["", "> Chọn **một** failure đau nhất ở trên để sửa prompt, "
                 "rồi chạy lại **trọn bộ** (guide §4.1)."]

    path.write_text("\n".join(dong) + "\n", encoding="utf-8")

    print(f"\nĐúng mức {dung_muc}/{tong} = {dung_muc/tong*100:.1f}% "
          f"· recall NGAY {recall_ngay*100:.0f}% · bịa {so_bia}")
    print(f"{'ĐẠT' if dat_bar else 'CHƯA ĐẠT'} quality bar → {path}")


if __name__ == "__main__":
    main()
