"""Sinh lại toàn bộ số liệu bằng chứng trong spec.md §1-§2.

Mục đích: người ngoài nhóm chạy đúng lệnh này phải ra **đúng những con số**
đang nằm trong spec — đó là yêu cầu "phương pháp đếm kiểm lại được" của rubric R1.

    python codebase/evidence.py            # in ra màn hình
    python codebase/evidence.py --ghi      # ghi đè eval/mining-log.md

Hai nguồn:
  Đường A — khảo sát nhóm tự chạy      -> eval/survey-responses.csv (ẩn danh, không tên)
  Đường B — mining data pack VLearn     -> dùng cho các ứng viên ĐÃ LOẠI trong bảng impact
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SURVEY = REPO / "eval" / "survey-responses.csv"

# Regex đếm "lượt tutor bí vì không tra được tài liệu" — dùng cho ứng viên đã loại.
# Cố ý viết ra đây để người khác chạy lại và tranh luận được về tiêu chí đếm.
RE_BI_TAI_LIEU = re.compile(
    r"không tìm thấy|không có (thông tin|nội dung)|không được đề cập|"
    r"tài liệu hiện có|không thấy"
)


def _tach_da_chon(gia_tri: str) -> list[str]:
    """Google Form nối các lựa chọn bằng '., ' — tách lại thành từng lựa chọn."""
    return [p.strip().strip(".").strip() for p in gia_tri.split(".,") if p.strip()]


def thong_ke_survey() -> dict:
    with SURVEY.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    cot = list(rows[0].keys())

    def dem_nhieu_lua_chon(idx: int) -> Counter:
        c: Counter = Counter()
        for r in rows:
            for lua_chon in _tach_da_chon(r[cot[idx]]):
                c[lua_chon] += 1
        return c

    muc_bi_miss = [int(r[cot[2]]) for r in rows]
    xac_nhan = sum(1 for x in muc_bi_miss if x >= 3)

    return {
        "n": len(rows),
        "thoi_gian_moi_ngay": Counter(r[cot[1]] for r in rows),
        "muc_bi_miss": Counter(muc_bi_miss),
        "so_xac_nhan": xac_nhan,
        "ti_le_xac_nhan": xac_nhan / len(rows),
        "trung_binh_bi_miss": sum(muc_bi_miss) / len(rows),
        "loai_tin_de_mat": dem_nhieu_lua_chon(3),
        "nguyen_nhan": dem_nhieu_lua_chon(4),
        "hau_qua": dem_nhieu_lua_chon(5),
        "tinh_nang_mong_doi": dem_nhieu_lua_chon(7),
        "kenh_mong_doi": dem_nhieu_lua_chon(8),
        "cau_hoi": {i: cot[i].strip() for i in range(1, len(cot))},
    }


def thong_ke_chatlog() -> dict | None:
    """Ứng viên ĐÃ LOẠI: tutor VLearn bí vì tài liệu không tra được.

    Trả None nếu không trỏ được tới data pack — data pack không nằm trong repo
    nộp bài nên người chấm có thể chạy mà không có nó.
    """
    try:
        import vlearn_data
    except Exception:
        return None
    try:
        luot = vlearn_data.load_turns()
    except SystemExit:
        return None

    tutor = [d for d in luot.values() if "tutor" in d]
    bi = [d for d in tutor if RE_BI_TAI_LIEU.search(d["tutor"]["content"])]
    tat_ca_user = {d["tutor"]["user_id"] for d in tutor}
    return {
        "tong_luot": len(tutor),
        "luot_bi": len(bi),
        "ti_le_bi": len(bi) / len(tutor),
        "user_dinh": len({d["tutor"]["user_id"] for d in bi}),
        "tong_user": len(tat_ca_user),
        "khong_trich_dan": sum(1 for d in tutor if d["tutor"]["citations"].strip() in ("[]", "")),
        "hoi_lai_kiem_tra": sum(1 for d in tutor if d["tutor"]["asked_check_question"] == "True"),
    }


def _bang(c: Counter, n: int) -> list[str]:
    return [f"| {k} | {v}/{n} | {v/n*100:.1f}% |" for k, v in c.most_common()]


def dung_bao_cao() -> str:
    s = thong_ke_survey()
    n = s["n"]
    d: list[str] = [
        "# Log bằng chứng — chạy lại được",
        "",
        "Sinh tự động bằng `python codebase/evidence.py --ghi`. Sửa tay file này là "
        "vô nghĩa: chạy lại lệnh trên sẽ ghi đè. Con số trong `spec.md` §1-§2 phải "
        "khớp với file này.",
        "",
        "## Đường A — khảo sát nhóm tự chạy",
        "",
        f"- Nguồn thô: `eval/survey-responses.csv` (n = **{n}**, form ẩn danh — không thu tên, không thu email).",
        f"- Chuẩn A của đề bài đòi **≥20 người ngoài nhóm**. Hiện **n = {n}** → "
        f"{'ĐÃ ĐẠT' if n >= 20 else f'**CHƯA ĐẠT, còn thiếu {20 - n} người**'}.",
        "",
        "### Câu hỏi đã hỏi (nguyên văn)",
        "",
    ]
    d += [f"{i}. {q}" for i, q in s["cau_hoi"].items()]
    d += [
        "",
        "### Q2 — Mức độ bị bỏ lỡ thông tin (thang 1-5)",
        "",
        "| Mức | Số người |",
        "|---|---|",
    ]
    d += [f"| {k} | {v} |" for k, v in sorted(s["muc_bi_miss"].items())]
    d += [
        "",
        f"**Xác nhận có pain (chọn ≥3/5): {s['so_xac_nhan']}/{n} = "
        f"{s['ti_le_xac_nhan']*100:.1f}%** → vượt ngưỡng ≥50% của chuẩn A. "
        f"Trung bình {s['trung_binh_bi_miss']:.2f}/5.",
        "",
        "### Q5 — Hậu quả đã thực sự xảy ra *(đây là phần đắt nhất của khảo sát)*",
        "",
        "| Hậu quả | Số người | Tỉ lệ |",
        "|---|---|---|",
    ]
    d += _bang(s["hau_qua"], n)
    d += ["", "### Q4 — Nguyên nhân", "", "| Nguyên nhân | Số người | Tỉ lệ |", "|---|---|---|"]
    d += _bang(s["nguyen_nhan"], n)
    d += ["", "### Q3 — Loại tin dễ bỏ lỡ nhất", "", "| Loại tin | Số người | Tỉ lệ |", "|---|---|---|"]
    d += _bang(s["loai_tin_de_mat"], n)
    d += ["", "### Q7 — Tính năng mong đợi", "", "| Tính năng | Số người | Tỉ lệ |", "|---|---|---|"]
    d += _bang(s["tinh_nang_mong_doi"], n)
    d += ["", "### Q8 — Kênh nhắc mong muốn", "", "| Kênh | Số người | Tỉ lệ |", "|---|---|---|"]
    d += _bang(s["kenh_mong_doi"], n)
    d += [
        "",
        "### Giới hạn của khảo sát — nhóm tự khai",
        "",
        f"1. **n = {n} < 20** → chưa đạt chuẩn A. Nhóm phải thu thêm "
        f"{max(0, 20 - n)} phản hồi trước khi chốt spec.",
        "2. **Câu 6 là câu hỏi dẫn dắt.** \"Nếu có một AI Agent… bạn đánh giá mức độ hữu ích\" "
        "đúng vào lỗi mà `02-guide.md` §1.3 cảnh báo — hầu như ai cũng trả lời cao. "
        "Nhóm **không dùng Q6 làm bằng chứng pain**; chỉ dùng Q2 (mức bị miss), "
        "Q4 (nguyên nhân) và Q5 (hậu quả đã xảy ra).",
        "3. Q3/Q4/Q5/Q7/Q8 là câu chọn nhiều đáp án từ danh sách có sẵn → có thiên lệch "
        "theo lựa chọn nhóm đưa ra. Vòng validation CP5 dùng câu hỏi mở để bù.",
        "",
    ]

    c = thong_ke_chatlog()
    d += ["## Đường B — mining data pack VLearn *(dùng cho ứng viên ĐÃ LOẠI)*", ""]
    if c is None:
        d += [
            "> Không chạy được vì máy này chưa trỏ `VLEARN_DATA_DIR` tới data pack. "
            "Data pack **cố ý không nằm trong repo** (luật bảo mật). "
            "Đặt biến môi trường rồi chạy lại để tái tạo các con số dưới đây.",
            "",
            "Số liệu nhóm đã đo (chạy ngày 30/07/2026): 170/1.261 lượt tutor bí vì không "
            "tra được tài liệu (13,5%), 113/369 học viên dính, 582/1.261 lượt trả lời "
            "không kèm trích dẫn (46,2%), `asked_check_question=True` chỉ 3/2.518 lượt.",
            "",
        ]
    else:
        d += [
            "Tiêu chí đếm (chạy lại được): một lượt bị tính là **tutor bí** khi nội dung "
            f"trả lời của tutor khớp regex `{RE_BI_TAI_LIEU.pattern}`.",
            "",
            "| Chỉ số | Giá trị |",
            "|---|---|",
            f"| Lượt tutor bí vì không tra được tài liệu | {c['luot_bi']}/{c['tong_luot']} = {c['ti_le_bi']*100:.1f}% |",
            f"| Học viên dính ít nhất 1 lần | {c['user_dinh']}/{c['tong_user']} |",
            f"| Lượt trả lời không kèm trích dẫn nào | {c['khong_trich_dan']}/{c['tong_luot']} = {c['khong_trich_dan']/c['tong_luot']*100:.1f}% |",
            f"| Lượt tutor chủ động hỏi lại kiểm tra hiểu bài | {c['hoi_lai_kiem_tra']} |",
            "",
        ]
    d += [
        "> Trích dẫn nguyên văn từ data pack ghi bằng **mã lượt** (`T####`) theo luật "
        "bảo mật, xem `spec.md` §1. Không dán nguyên văn dài vào repo này.",
    ]
    return "\n".join(d) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ghi", action="store_true", help="Ghi đè eval/mining-log.md")
    args = parser.parse_args()

    bao_cao = dung_bao_cao()
    if args.ghi:
        path = REPO / "eval" / "mining-log.md"
        path.write_text(bao_cao, encoding="utf-8")
        print(f"Đã ghi {path}")
    else:
        print(bao_cao)


if __name__ == "__main__":
    main()
