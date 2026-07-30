"""EVALUATE + DECIDE — quyết định trung tâm, chạy bằng lời gọi AI thật.

Vòng lặp của note.txt thu về đúng một ngày Discord:
    OBSERVE  (corpus.py nạp tin trong ngày)
 -> EVALUATE (LLM đọc từng tin trong ngữ cảnh cả ngày)
 -> DECIDE   (chọn 1 trong 4 mức NGAY / HOM_NAY / GHI_NHO / BO_QUA)
 -> ACT      (digest.py dựng bản tin)
 -> LEARN    (app.py ghi 👍👎 + "sai chỗ nào" vào logs/feedback.jsonl)

LLM quyết định mức. Code KHÔNG đoán hộ — code chỉ chặn 4 kiểu sai mà hậu quả
không sửa được (xem GUARDS bên dưới).
"""

from __future__ import annotations

import json
import os
import re
import time
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

try:  # .env là tuỳ chọn — chạy được cả khi export biến môi trường bằng tay
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:  # pragma: no cover
    pass

CODEBASE = Path(__file__).resolve().parent
PROMPT_PATH = CODEBASE / "prompts" / "triage.md"
LOG_DIR = CODEBASE / "logs"

MUC_HOP_LE = ("NGAY", "HOM_NAY", "GHI_NHO", "BO_QUA")
THU_TU_MUC = {m: i for i, m in enumerate(MUC_HOP_LE)}  # 0 = gấp nhất
NGUON_CHINH_THUC = {"giang_vien", "ta", "admin"}

# Chỉ những trường này được gửi cho LLM. `_bay` (nhãn vàng) không bao giờ lọt vào.
TRUONG_GUI_LLM = ("id", "ts", "kenh", "tac_gia", "vai", "noi_dung", "tra_loi_cho")

# Thử lại khi API trả lỗi tạm thời: chờ 5s, 10s, 20s, 40s giữa các lần.
SO_LAN_THU = 5
CHO_BAN_DAU_GIAY = 5


@dataclass
class KetLuan:
    """Kết luận cuối cùng cho một tin — sau khi guard đã can thiệp."""

    id: str
    muc: str
    viec_can_lam: str | None
    han_chot: str | None
    trich_dan: str | None
    do_chac: str
    hoi_ta: str | None
    vi_sao: str
    muc_llm: str  # mức LLM đề xuất, trước guard
    co: list[str] = field(default_factory=list)  # guard nào đã can thiệp

    @property
    def bi_ha_cap(self) -> bool:
        return self.muc != self.muc_llm


def _chuan_hoa(text: str) -> str:
    """So khớp trích dẫn bỏ qua khác biệt dấu cách / unicode / hoa thường."""
    text = unicodedata.normalize("NFC", text or "").lower()
    return re.sub(r"\s+", " ", text).strip()


def _ha_muc(muc: str, tran: str) -> str:
    """Không cho mức gấp hơn `tran`."""
    return muc if THU_TU_MUC[muc] >= THU_TU_MUC[tran] else tran


def ap_guard(tin_theo_id: dict[str, dict], items: list[dict]) -> list[KetLuan]:
    """Bốn guard tất định. Mỗi cái chặn một kiểu sai có hậu quả không sửa được.

    G-A  id không có thật        -> bỏ hẳn phần tử (LLM bịa tin)
    G-B  trích dẫn không khớp    -> hạ GHI_NHO + do_chac thấp (LLM bịa căn cứ)
    G-C  hạn chót không căn cứ   -> xoá hạn chót (nhắc sai hạn = nộp muộn, mất điểm)
    G-D  nguồn không chính thức  -> hạ GHI_NHO + bắt buộc hỏi TA (tin đồn ≠ thông báo)
    """
    ket_luan: list[KetLuan] = []
    for item in items:
        msg_id = str(item.get("id", "")).strip()
        tin = tin_theo_id.get(msg_id)
        if tin is None:
            continue  # G-A

        co: list[str] = []
        muc_llm = str(item.get("muc", "")).strip().upper()
        muc = muc_llm if muc_llm in MUC_HOP_LE else "BO_QUA"
        if muc != muc_llm:
            co.append("muc_khong_hop_le")

        do_chac = "thap" if str(item.get("do_chac", "")).strip() != "cao" else "cao"
        trich_dan = item.get("trich_dan") or None
        han_chot = item.get("han_chot") or None
        hoi_ta = item.get("hoi_ta") or None
        viec_can_lam = item.get("viec_can_lam") or None

        # G-B — trích dẫn phải là chuỗi con nguyên văn của chính tin đó.
        # Trích dẫn bịa thì câu "việc cần làm" dựng trên nó cũng không tin được,
        # nên phải gỡ luôn — hạ mức mà giữ nguyên câu sai là vẫn lừa người đọc.
        if trich_dan and _chuan_hoa(trich_dan) not in _chuan_hoa(tin["noi_dung"]):
            co.append("trich_dan_khong_khop")
            trich_dan = None
            viec_can_lam = None
            do_chac = "thap"
            muc = _ha_muc(muc, "GHI_NHO")

        # G-C — hạn chót phải tựa trên một trích dẫn có thật
        if han_chot and not trich_dan:
            co.append("han_chot_khong_can_cu")
            han_chot = None
            do_chac = "thap"

        # G-D — chỉ GV/TA/Admin mới đặt được lịch và hạn chót
        if tin.get("vai") not in NGUON_CHINH_THUC and THU_TU_MUC[muc] < THU_TU_MUC["GHI_NHO"]:
            co.append("nguon_khong_chinh_thuc")
            muc = "GHI_NHO"
            do_chac = "thap"
            han_chot = None
            # Câu hành động dựng trên tin đồn còn nguy hiểm hơn cả mức khẩn sai
            # ("Yên tâm, deadline đã dời") — thay bằng lời nhắc kiểm chứng.
            viec_can_lam = "Có tin chưa xác nhận liên quan đến lịch/hạn nộp — hỏi TA trước khi tin."
            hoi_ta = hoi_ta or (
                "Tin này do bạn học chia sẻ, chưa có xác nhận chính thức — "
                "nhờ TA xác nhận giúp mình được không ạ?"
            )

        ket_luan.append(
            KetLuan(
                id=msg_id,
                muc=muc,
                viec_can_lam=viec_can_lam,
                han_chot=han_chot,
                trich_dan=trich_dan,
                do_chac=do_chac,
                hoi_ta=hoi_ta,
                vi_sao=item.get("vi_sao") or "",
                muc_llm=muc_llm,
                co=co,
            )
        )
    return ket_luan


def dung_prompt(messages: list[dict], ngay_tham_chieu: str) -> str:
    mau = PROMPT_PATH.read_text(encoding="utf-8")
    goi = [{k: m[k] for k in TRUONG_GUI_LLM if k in m} for m in messages]
    return mau.replace("{NGAY_THAM_CHIEU}", ngay_tham_chieu).replace(
        "{MESSAGES_JSON}", json.dumps(goi, ensure_ascii=False, indent=2)
    )


def _tach_json(text: str) -> list[dict]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    data = json.loads(text)
    if isinstance(data, dict):  # model thỉnh thoảng bọc trong {"ket_qua": [...]}
        for value in data.values():
            if isinstance(value, list):
                return value
        raise ValueError("Không tìm thấy mảng JSON trong output")
    return data


def _ma_loi(loi: Exception) -> str:
    return str(getattr(loi, "code", "") or getattr(loi, "status_code", "") or "lỗi mạng")


def _loi_tam_thoi(loi: Exception) -> bool:
    """503 quá tải, 429 chạm quota phút, 500/504 lỗi tạm phía Google."""
    ma = _ma_loi(loi)
    return ma in {"429", "500", "503", "504", "lỗi mạng"}


def goi_llm(prompt: str) -> tuple[str, dict]:
    """Lời gọi AI THẬT ở quyết định trung tâm. Không có fallback hardcode."""
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Thiếu GOOGLE_API_KEY.\n"
            "Lấy key miễn phí tại https://aistudio.google.com/apikey rồi đặt vào .env "
            "(xem .env.example). Prototype cố ý KHÔNG có đường chạy giả — "
            "quyết định trung tâm bắt buộc do AI thật đưa ra."
        )

    from google import genai
    from google.genai import types

    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        temperature=0,  # quyết định phải lặp lại được giữa các lượt đo
        response_mime_type="application/json",
    )

    # Free tier hay trả 503 (model quá tải) / 429 (chạm quota phút) — đây là
    # nhiễu hạ tầng, không phải kết quả đo. Lùi dần rồi thử lại thay vì để cả
    # lượt chạy trọn bộ đổ vì một lời gọi xui.
    bat_dau = time.perf_counter()
    for lan in range(SO_LAN_THU):
        try:
            resp = client.models.generate_content(
                model=model, contents=prompt, config=config
            )
            break
        except Exception as loi:  # SDK không tách riêng lỗi tạm thời
            if not _loi_tam_thoi(loi) or lan == SO_LAN_THU - 1:
                raise
            cho = CHO_BAN_DAU_GIAY * 2**lan
            print(
                f"  ⟳ {_ma_loi(loi)} từ '{model}' — chờ {cho}s rồi thử lại "
                f"(lần {lan + 2}/{SO_LAN_THU})…"
            )
            time.sleep(cho)

    do_tre_ms = int((time.perf_counter() - bat_dau) * 1000)
    return resp.text, {"model": model, "do_tre_ms": do_tre_ms, "so_lan_goi": lan + 1}


def phan_loai_ngay(
    messages: list[dict], ngay_tham_chieu: str, ten_lo: str = "adhoc"
) -> tuple[list[KetLuan], dict]:
    """Chạy trọn một ngày: 1 lời gọi AI cho cả ngày, rồi áp guard."""
    prompt = dung_prompt(messages, ngay_tham_chieu)
    raw, meta = goi_llm(prompt)
    items = _tach_json(raw)
    tin_theo_id = {m["id"]: m for m in messages}
    ket_luan = ap_guard(tin_theo_id, items)

    thieu = [m["id"] for m in messages if m["id"] not in {k.id for k in ket_luan}]
    meta = {
        **meta,
        "prompt_version": _doc_version(),
        "ten_lo": ten_lo,
        "ngay_tham_chieu": ngay_tham_chieu,
        "so_tin_vao": len(messages),
        "so_ket_luan": len(ket_luan),
        "id_bi_bo_sot": thieu,
        "so_lan_guard_can_thiep": sum(1 for k in ket_luan if k.co),
    }
    ghi_trace(prompt, raw, ket_luan, meta)
    return ket_luan, meta


def ghi_trace(prompt: str, raw: str, ket_luan: list[KetLuan], meta: dict) -> None:
    """Trace đầy đủ để TA kiểm 'AI thật, không hardcode' tại CP3/CP5."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ban_ghi = {
        "thoi_diem": datetime.now().astimezone().isoformat(timespec="seconds"),
        "meta": meta,
        "prompt_version": _doc_version(),
        "prompt_ky_tu": len(prompt),
        "output_tho": raw,
        "sau_guard": [k.__dict__ for k in ket_luan],
    }
    with (LOG_DIR / "trace.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(ban_ghi, ensure_ascii=False) + "\n")


def _doc_version() -> str:
    dong_dau = PROMPT_PATH.read_text(encoding="utf-8").splitlines()[0]
    match = re.search(r"version:\s*(\S+)", dong_dau)
    return match.group(1) if match else "?"
