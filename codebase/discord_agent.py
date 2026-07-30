"""Grounded Gemini triage for local Discord announcement exports."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISCORD_DIR = ROOT / "data" / "discord-pack"
TRACE_PATH = Path(__file__).resolve().parent / "logs" / "agent_runs.jsonl"


def load_announcements() -> list[dict[str, str]]:
    """Split each export into reviewable, traceable announcement blocks."""
    announcements = []
    for path in sorted(DISCORD_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig").strip()
        blocks = [item.strip() for item in re.split(r"\n\s*\n\s*\n+", text) if item.strip()]
        for index, block in enumerate(blocks, start=1):
            announcements.append({"id": f"{path.name}#{index}", "source": path.name, "text": block})
    return announcements


def _prompt(announcements: list[dict[str, str]], reference_date: str) -> str:
    payload = "\n\n".join(
        f"[SOURCE {item['id']}]\n{item['text']}" for item in announcements
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


def _extract_json(response: dict) -> dict:
    try:
        text = response["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError("Gemini did not return valid structured JSON.") from error


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


def scan(reference_date: str) -> tuple[dict, int]:
    """Make one real Gemini call, then apply deterministic grounding guards."""
    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    if not api_key:
        raise RuntimeError("Thiếu GOOGLE_API_KEY. Hãy thêm key vào codebase/.env.")
    announcements = load_announcements()
    if not announcements:
        raise RuntimeError("Không tìm thấy file .txt trong data/discord-pack.")
    request_body = json.dumps({
        "contents": [{"parts": [{"text": _prompt(announcements, reference_date)}]}],
        "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json", "maxOutputTokens": 8192},
    }).encode("utf-8")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + urllib.parse.quote(model, safe="-_.") + ":generateContent"
    request = urllib.request.Request(endpoint, data=request_body, headers={"Content-Type": "application/json", "x-goog-api-key": api_key}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=90) as raw:
            result = _extract_json(json.loads(raw.read().decode("utf-8")))
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Gemini API returned HTTP {error.code}.") from error
    except urllib.error.URLError as error:
        raise RuntimeError("Không kết nối được Gemini API. Kiểm tra mạng hoặc API key.") from error
    grounded = _ground(result, {item["id"]: item["text"] for item in announcements})
    TRACE_PATH.parent.mkdir(exist_ok=True)
    with TRACE_PATH.open("a", encoding="utf-8") as trace:
        trace.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "model": model, "source_count": len(announcements), "actions": len(grounded["action_items"]), "needs_confirmation": len(grounded["needs_confirmation"])}) + "\n")
    return grounded, len(announcements)
