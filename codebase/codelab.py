"""Giả lập API kiểm tra trạng thái nộp bài trên Codelabs.

Mỗi ngày lab mở lúc 09:00 và đóng lúc 23:59 cùng ngày, nên câu hỏi "mình nộp
chưa?" là việc phải trả lời trước khi hết ngày. Prototype chưa có quyền truy
cập Codelabs thật, vì vậy module này đóng vai adapter: cùng chữ ký và cùng hình
dạng dữ liệu như một API thật, nhưng đọc/ghi trạng thái ở `store/codelab.json`
để demo được cả hai nhánh (chưa nộp → nộp → xác nhận).

Khi có API thật, chỉ cần thay ruột `check_submission()`; phần UI không đổi.
"""

from __future__ import annotations

import json
import time
from datetime import date, datetime, timezone
from pathlib import Path

STORE_PATH = Path(__file__).resolve().parent / "store" / "codelab.json"

CODELAB_URL = "https://codelabs.vlearn.dev/codelab"
OPEN_AT = "09:00"
DUE_AT = "23:59"
SOURCE = "codelabs.vlearn.dev (API giả lập)"
LATENCY_SECONDS = 0.4  # để spinner phản ánh đúng việc đây là một lượt gọi mạng


def lab_of(reference_date: str) -> dict:
    """Bài lab tương ứng ngày tham chiếu. Không bịa tên lab — đặt tên theo ngày."""
    day = date.fromisoformat(reference_date)
    return {
        "lab_id": f"lab-{day.isoformat()}",
        "lab_title": f"Lab ngày {day.strftime('%d/%m')}",
        "open_at": OPEN_AT,
        "due_at": DUE_AT,
    }


def _read_state() -> dict:
    if not STORE_PATH.exists():
        return {}
    try:
        data = json.loads(STORE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _write_state(state: dict) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _key(student_id: str, reference_date: str) -> str:
    return f"{student_id}|{reference_date}"


def check_submission(student_id: str, reference_date: str) -> dict:
    """Trả lời đúng một câu: học viên đã nộp lab của ngày này chưa?

    Mặc định là CHƯA nộp — đó mới là nhánh cần nhắc. Trạng thái chỉ chuyển sang
    đã nộp khi người dùng xác nhận qua `confirm_submission()`.
    """
    time.sleep(LATENCY_SECONDS)
    record = _read_state().get(_key(student_id, reference_date), {})
    lab = lab_of(reference_date)
    return {
        **lab,
        "student_id": student_id,
        "reference_date": reference_date,
        "submitted": bool(record.get("submitted")),
        "confirmed_at": record.get("confirmed_at"),
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url": CODELAB_URL,
        "source": SOURCE,
    }


def confirm_submission(student_id: str, reference_date: str) -> dict:
    """Người dùng xác nhận đã nộp trên Codelabs; kiểm tra lại để lấy trạng thái mới."""
    state = _read_state()
    state[_key(student_id, reference_date)] = {
        "submitted": True,
        "confirmed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    _write_state(state)
    return check_submission(student_id, reference_date)


def reset() -> None:
    _write_state({})
