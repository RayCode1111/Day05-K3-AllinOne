"""Grounded Gemini triage for local Discord announcement exports."""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import discord_store

TRACE_PATH = Path(__file__).resolve().parent / "logs" / "agent_runs.jsonl"
CACHE_PATH = Path(__file__).resolve().parent / "store" / "scan_cache.json"
BAD_RESPONSE_PATH = Path(__file__).resolve().parent / "store" / "last_bad_response.txt"

# Chuỗi model dự phòng: mỗi model có hạn mức free-tier riêng theo ngày, và mọi
# model ở đây đều cho phép output tối thiểu 16k token nên không sợ bị cắt.
DEFAULT_MODELS = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"]
MAX_RETRY_WAIT = 30  # giây — chờ lâu hơn thì đổi model nhanh hơn là ngồi đợi


def load_announcements() -> list[dict[str, str]]:
    """Mọi thông báo Nova được đọc: data pack + thông báo mới đẩy lên lúc chạy."""
    return discord_store.all_messages()


def _prompt(announcements: list[dict[str, str]], reference_date: str) -> str:
    payload = "\n\n".join(
        f"[SOURCE {item['id']} | kênh #{item['channel']} | người gửi: {item['author']}"
        f"{' | ngày đăng: ' + item['date'] if item.get('date') else ''}]\n{item['text']}"
        for item in announcements
    )
    return f"""Bạn là Nova, trợ lý học viên cho Discord của khóa học.
Ngày tham chiếu là {reference_date}. Hãy đọc duy nhất dữ liệu nguồn bên dưới.

Mục tiêu: tổng hợp thông báo quan trọng thành danh sách công việc có thể hành động.
Đây là quyết định có cost-of-error cao: sai deadline có thể làm học viên mất điểm.

QUY TẮC BẮT BUỘC:
1. Không bịa deadline, link, tác giả, kênh, hay trạng thái hoàn thành.
2. Mỗi action phải có đúng một source_id và evidence là đoạn trích ngắn NGUYÊN VĂN từ nguồn đó.
3. Chỉ gán confidence="high" khi evidence nêu rõ hành động/thời hạn hoặc thông tin có dấu hiệu thông báo chính thức (BTC, THÔNG BÁO, @Learner). Nếu mơ hồ, đưa vào needs_confirmation.
4. Nếu nguồn tự mâu thuẫn (ví dụ hai ngày khác nhau) hoặc chỉ nói “hôm nay” mà không xác định được ngày, không tự suy diễn; đưa needs_confirmation và nêu câu hỏi cho TA/BTC.
5. Bỏ qua quảng cáo, lời cảm ơn, cập nhật kỹ thuật không đòi hỏi học viên hành động.
6. Gộp các thông báo lặp nhưng vẫn giữ evidence/source_id tốt nhất.

Trả về JSON thuần theo format:
{{
 "summary": "tóm tắt tối đa 70 từ bằng tiếng Việt",
 "action_items": [{{"id":"ngắn-gọn", "title":"động từ + việc", "priority":"urgent|today|upcoming", "deadline":"chuỗi nguyên văn hoặc null", "detail":"tối đa 25 từ", "source_id":"...", "evidence":"trích nguyên văn", "confidence":"high|medium"}}],
 "needs_confirmation": [{{"title":"...", "source_id":"...", "evidence":"...", "question":"câu hỏi ngắn cần gửi TA/BTC"}}],
 "ignored_count": 0
}}

NGUỒN:
{payload}"""


def _answer_text(candidate: dict) -> str:
    """Ghép phần trả lời, bỏ qua phần suy nghĩ của model.

    Model dòng thinking có thể trả thêm part `thought=true` chứa văn xuôi. Ghép
    cả phần đó vào rồi mới parse thì JSON hợp lệ cũng hoá thành rác.
    """
    parts = candidate.get("content", {}).get("parts") or []
    return "".join(part.get("text", "") for part in parts if not part.get("thought")).strip()


def _json_block(text: str) -> str:
    """Cắt lấy khối JSON ngoài cùng, bỏ rào ```json và mọi lời dẫn quanh nó."""
    fenced = re.search(r"```(?:json)?\s*(.+?)\s*```", text, re.S)
    if fenced:
        text = fenced.group(1)
    start, end = text.find("{"), text.rfind("}")
    return text[start:end + 1] if 0 <= start < end else ""


def _extract_json(response: dict) -> dict:
    """Đọc JSON từ phản hồi và nói rõ hỏng ở đâu khi không đọc được.

    Hai nguyên nhân hay gặp — phản hồi bị cắt giữa chừng
    (`finishReason=MAX_TOKENS`) và model kèm lời dẫn quanh JSON — cần thông báo
    khác nhau, vì một cái phải tăng token còn một cái chỉ cần bóc lại chuỗi.
    """
    candidate = (response.get("candidates") or [{}])[0]
    reason = candidate.get("finishReason")
    text = _answer_text(candidate)
    if not text:
        raise RuntimeError(f"Gemini trả về phản hồi rỗng (finishReason={reason}). Hãy thử lại.")
    for attempt in (text, _json_block(text)):
        if not attempt:
            continue
        try:
            return json.loads(attempt)
        except json.JSONDecodeError:
            continue
    _dump_bad_response(text, reason)
    if reason == "MAX_TOKENS":
        raise RuntimeError("Phản hồi của Gemini bị cắt vì vượt giới hạn token; tăng GEMINI_MAX_OUTPUT_TOKENS rồi thử lại.")
    raise RuntimeError(f"Gemini không trả về JSON hợp lệ (finishReason={reason}, đầu phản hồi: “{text[:80]}…”).")


def _dump_bad_response(text: str, reason: str | None) -> None:
    """Ghi lại phản hồi không parse được để còn soi khi cần, không làm sập app."""
    try:
        BAD_RESPONSE_PATH.parent.mkdir(parents=True, exist_ok=True)
        BAD_RESPONSE_PATH.write_text(f"finishReason={reason}\nat={datetime.now(timezone.utc).isoformat()}\n\n{text}", encoding="utf-8")
    except OSError:
        pass


def _ground(result: dict, sources: dict[str, str]) -> dict:
    """Reject AI fields which cannot be traced back to an exact local source."""
    valid_items, confirmations = [], []
    for item in result.get("action_items", []):
        source_id, evidence = item.get("source_id", ""), item.get("evidence", "")
        if item.get("confidence") == "high" and source_id in sources and evidence and evidence in sources[source_id]:
            item["priority"] = item.get("priority") if item.get("priority") in {"urgent", "today", "upcoming"} else "today"
            valid_items.append(item)
        else:
            confirmations.append({"title": item.get("title", "Thông tin chưa xác thực"), "source_id": source_id, "evidence": evidence, "question": "Bạn có thể kiểm tra lại với TA/BTC không?"})
    for item in result.get("needs_confirmation", []):
        if item.get("source_id") in sources:
            confirmations.append(item)
    result["action_items"] = valid_items
    result["needs_confirmation"] = confirmations
    return result


def _models() -> list[str]:
    """Danh sách model thử lần lượt.

    Hạn mức free-tier của Gemini tính theo TỪNG MODEL mỗi ngày
    (`GenerateRequestsPerDayPerProjectPerModel`), nên khi model chính hết quota,
    chuyển sang model khác là cách duy nhất chạy tiếp mà không cần nâng cấp gói.
    """
    raw = os.getenv("GEMINI_MODELS") or ""
    chain = [name.strip() for name in raw.split(",") if name.strip()]
    if not chain:
        chain = [os.getenv("GEMINI_MODEL", DEFAULT_MODELS[0])] + DEFAULT_MODELS
    seen, ordered = set(), []
    for name in chain:  # giữ thứ tự ưu tiên, bỏ trùng
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def _quota_kind(payload: dict) -> tuple[str, float]:
    """Đọc chi tiết lỗi quota: giới hạn theo phút hay theo ngày, chờ bao lâu."""
    kind, delay = "", 0.0
    for detail in payload.get("error", {}).get("details", []):
        marker = str(detail.get("@type", ""))
        if marker.endswith("QuotaFailure"):
            for violation in detail.get("violations", []):
                quota_id = str(violation.get("quotaId", ""))
                kind = "minute" if "PerMinute" in quota_id else "day" if "PerDay" in quota_id else kind
        elif marker.endswith("RetryInfo"):
            try:
                delay = float(str(detail.get("retryDelay", "0s")).rstrip("s"))
            except ValueError:
                delay = 0.0
    return kind, delay


def _generate(request_body: bytes, api_key: str) -> tuple[dict, str]:
    """Gọi Gemini rồi parse JSON, đổi model khi model hiện tại không dùng được.

    Hết quota, mất mạng hay trả về JSON hỏng đều được xử lý như nhau: model này
    không xong thì sang model kế tiếp, chỉ báo lỗi khi cả chuỗi đều thất bại.
    """
    problems = []
    for model in _models():
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + urllib.parse.quote(model, safe="-_.") + ":generateContent"
        request = urllib.request.Request(endpoint, data=request_body, headers={"Content-Type": "application/json", "x-goog-api-key": api_key}, method="POST")
        for attempt in range(2):
            try:
                with urllib.request.urlopen(request, timeout=120) as raw:
                    return _extract_json(json.loads(raw.read().decode("utf-8"))), model
            except RuntimeError as error:  # phản hồi rỗng / bị cắt / không phải JSON
                problems.append(f"{model}: {error}")
                break
            except urllib.error.HTTPError as error:
                try:
                    payload = json.loads(error.read().decode("utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    payload = {}
                kind, delay = _quota_kind(payload)
                # Giới hạn theo phút thì chờ đúng khoảng API yêu cầu rồi thử lại;
                # hết quota theo ngày thì chờ bao lâu cũng vô ích, đổi model luôn.
                if error.code == 429 and kind == "minute" and attempt == 0 and 0 < delay <= MAX_RETRY_WAIT:
                    time.sleep(delay)
                    continue
                problems.append(f"{model}: HTTP {error.code}" + (" (hết quota ngày)" if kind == "day" else ""))
                break
            except urllib.error.URLError:
                problems.append(f"{model}: không kết nối được")
                break
    raise RuntimeError(
        "Chưa model nào trả lời được — " + "; ".join(problems)
        + ". Hạn mức free-tier tính riêng cho từng model mỗi ngày: thêm model dự phòng vào GEMINI_MODELS trong .env, dùng API key khác, hoặc chờ quota reset."
    )


def _grounded_scan(request_body: bytes, api_key: str, sources: dict[str, str]) -> dict:
    result, model = _generate(request_body, api_key)
    grounded = _ground(result, sources)
    grounded["meta"] = {"model": model, "cached": False, "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    return grounded


def _cache_read(fingerprint: str) -> dict | None:
    if not CACHE_PATH.exists():
        return None
    try:
        cached = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return cached if cached.get("fingerprint") == fingerprint else None


def _cache_write(fingerprint: str, result: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps({"fingerprint": fingerprint, "result": result}, ensure_ascii=False), encoding="utf-8")


def clear_cache() -> None:
    CACHE_PATH.unlink(missing_ok=True)


def scan(reference_date: str, force: bool = False) -> tuple[dict, int]:
    """Rà soát thông báo bằng Gemini rồi áp guard grounding.

    Chỉ gọi API khi dữ liệu thật sự đổi: cùng ngày tham chiếu và cùng bộ thông
    báo thì dùng lại kết quả đã lưu. Mỗi lần bấm nút không được đốt một request
    — hạn mức free-tier chỉ 20 request/model/ngày.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Thiếu GOOGLE_API_KEY. Hãy thêm key vào codebase/.env.")
    announcements = load_announcements()
    if not announcements:
        raise RuntimeError("Chưa có thông báo nào để đọc: kiểm tra data/discord-pack hoặc đẩy thông báo qua cửa sổ Discord.")

    fingerprint = hashlib.sha256(json.dumps([reference_date] + [[item["id"], item["text"]] for item in announcements], ensure_ascii=False).encode("utf-8")).hexdigest()
    if not force:
        cached = _cache_read(fingerprint)
        if cached:
            result = cached["result"]
            result.setdefault("meta", {})["cached"] = True
            return result, len(announcements)

    # Mỗi action item mang theo evidence nguyên văn nên output dài theo số thông
    # báo; 8192 token đủ cho pack gốc nhưng bị cắt khi đẩy thêm thông báo mới.
    max_output_tokens = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "16384"))
    request_body = json.dumps({
        "contents": [{"parts": [{"text": _prompt(announcements, reference_date)}]}],
        "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json", "maxOutputTokens": max_output_tokens},
    }).encode("utf-8")
    grounded = _grounded_scan(request_body, api_key, {item["id"]: item["text"] for item in announcements})
    model = grounded["meta"]["model"]
    _cache_write(fingerprint, grounded)
    TRACE_PATH.parent.mkdir(exist_ok=True)
    with TRACE_PATH.open("a", encoding="utf-8") as trace:
        trace.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "model": model, "source_count": len(announcements), "actions": len(grounded["action_items"]), "needs_confirmation": len(grounded["needs_confirmation"])}) + "\n")
    return grounded, len(announcements)
