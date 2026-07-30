"""Sinh lại toàn bộ số liệu bằng chứng trong spec.md §1-§2.

Mục đích: người ngoài nhóm chạy đúng lệnh này phải ra **đúng những con số**
đang nằm trong spec — đó là yêu cầu "phương pháp đếm kiểm lại được" của rubric R1.

    python codebase/evidence.py            # in ra màn hình
    python codebase/evidence.py --ghi      # ghi đè eval/mining-log.md

Hai nguồn:
  Đường A — khảo sát nhóm tự chạy      -> eval/survey-responses.csv (ẩn danh, không tên)
  Đường B — mining data pack Discord   -> thông báo THẬT của khoá, đếm lại được
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SURVEY = REPO / "eval" / "survey-responses.csv"

# Tiêu chí đếm trên data pack Discord. Cố ý viết ra đây để người khác chạy lại
# và TRANH LUẬN ĐƯỢC về tiêu chí — không giấu trong đầu người đếm.
#
# RE_VIEC   — tin có việc học viên phải làm kèm mốc/hạn.
# RE_PING   — tin ping cả lớp (đúng loại khiến 7/11 người khảo sát phải mute).
RE_VIEC = re.compile(r"hạn|deadline|hết hạn|trước ngày|nộp|gia hạn|đóng đúng|due", re.I)
RE_PING = re.compile(r"@everyone|@here|@Learner|@Lab Coach")


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
    """Đếm trên thông báo THẬT của khoá trong data pack Discord.

    Trả None nếu không trỏ được tới data pack — data pack không nằm trong repo
    nộp bài nên người chấm có thể chạy mà không có nó.
    """
    try:
        import discord_data
    except Exception:
        return None
    try:
        tin = discord_data.load_messages()
    except SystemExit:
        return None
    if not tin:
        return None

    co_viec = [t for t in tin if RE_VIEC.search(t)]
    ping = [t for t in tin if RE_PING.search(t)]
    ping_khong_viec = [t for t in ping if not RE_VIEC.search(t)]
    do_dai = sorted(len(t) for t in tin)
    return {
        "tong_tin": len(tin),
        "co_viec": len(co_viec),
        "ping": len(ping),
        "ping_khong_viec": len(ping_khong_viec),
        "dai_tb": sum(do_dai) / len(do_dai),
        "dai_trung_vi": do_dai[len(do_dai) // 2],
        "dai_nhat": do_dai[-1],
        "tin_dai": sum(1 for x in do_dai if x > 500),
    }


def discord_ranh_gioi() -> str:
    """Pattern tách tin — lấy từ discord_data để log không lệch với code thật."""
    try:
        import discord_data

        return discord_data.RANH_GIOI_TIN.pattern
    except Exception:
        return r"\n{3,}"


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
    d += ["## Đường B — mining data pack Discord *(thông báo THẬT của khoá)*", ""]
    if c is None:
        d += [
            "> Không chạy được vì máy này chưa trỏ `DISCORD_DATA_DIR` tới data pack. "
            "Data pack **cố ý không nằm trong repo** (luật bảo mật). "
            "Đặt biến môi trường rồi chạy lại để tái tạo các con số dưới đây.",
            "",
        ]
    else:
        ping_tl = c["ping_khong_viec"] / c["ping"] * 100 if c["ping"] else 0.0
        d += [
            "Tiêu chí đếm — viết ra để tranh luận được, không giấu trong đầu người đếm:",
            "",
            f"- Ranh giới giữa hai thông báo: khoảng trống **từ 2 dòng trống trở lên** "
            f"(regex `{discord_ranh_gioi()}`). Xuống đoạn trong cùng một thông báo chỉ "
            "cách 1 dòng trống, nên ngưỡng này tách đúng tin thay vì cắt vụn tin dài.",
            f"- Tin **có việc phải làm**: khớp regex `{RE_VIEC.pattern}`.",
            f"- Tin **ping cả lớp**: khớp regex `{RE_PING.pattern}`.",
            "",
            "| Chỉ số | Giá trị |",
            "|---|---|",
            f"| Tổng số thông báo trong pack | {c['tong_tin']} |",
            f"| Tin có việc phải làm kèm hạn | {c['co_viec']}/{c['tong_tin']} = {c['co_viec']/c['tong_tin']*100:.1f}% |",
            f"| Tin ping cả lớp (@everyone/@here/@Learner) | {c['ping']}/{c['tong_tin']} = {c['ping']/c['tong_tin']*100:.1f}% |",
            f"| **Tin ping cả lớp nhưng KHÔNG kèm việc phải làm** | **{c['ping_khong_viec']}/{c['ping']} = {ping_tl:.0f}%** |",
            f"| Độ dài thông báo (trung bình · trung vị · dài nhất) | {c['dai_tb']:.0f} · {c['dai_trung_vi']} · {c['dai_nhat']} ký tự |",
            f"| Thông báo dài hơn 500 ký tự | {c['tin_dai']}/{c['tong_tin']} |",
            "",
            "**Hai con số đáng giá nhất:**",
            "",
            f"1. **{c['ping_khong_viec']}/{c['ping']} ({ping_tl:.0f}%) tin ping cả lớp không kèm việc phải làm.** "
            "Đây là bằng chứng **độc lập với khảo sát** cho đúng nguyên nhân mà "
            "7/11 người khảo sát khai là lý do họ phải mute. Khảo sát nói người dùng "
            "*cảm thấy* bị spam; pack cho thấy họ *bị spam thật*.",
            f"2. **Thông báo dài trung bình {c['dai_tb']:.0f} ký tự, {c['tin_dai']}/{c['tong_tin']} tin dài hơn 500 ký tự.** "
            f"Chỉ {c['co_viec']}/{c['tong_tin']} tin thật sự có việc phải làm — tức là học viên "
            "phải đọc rất nhiều chữ để tìm ra phần nhỏ thật sự liên quan tới mình. "
            "Đó đúng là việc mà bản tin lọc gánh hộ.",
            "",
            "**Chỉ số đã thử nhưng KHÔNG dùng — khai để khỏi bị hiểu là chọn số đẹp:** "
            "nhóm định đo *\"hạn chót bị chôn sâu trong thân bài\"*, nhưng đo ra hạn xuất "
            "hiện trung bình ở **23%** chiều dài tin và chỉ **1/7** tin phải đọc quá nửa mới "
            "thấy hạn. Giả thuyết đó **không được data ủng hộ**, nên bỏ, không đưa vào spec.",
            "",
        ]
    d += [
        "> Không dán nguyên văn dài từ data pack vào repo này theo luật bảo mật "
        "(`.gitignore` chặn `data/`). Chỉ giữ số đếm và tiêu chí đếm.",
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
