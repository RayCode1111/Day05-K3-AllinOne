"""Nạp data pack VLearn từ đường dẫn cấu hình bằng biến môi trường.

Data pack KHÔNG nằm trong repo này (luật bảo mật: không commit data pack vào
repo nộp bài). Mọi module khác đi qua đây để lấy đường dẫn, không hardcode.
"""

from __future__ import annotations

import csv
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:  # .env là tuỳ chọn — chạy được cả khi export biến môi trường bằng tay
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:  # pragma: no cover
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = "../Day05-K3-AllinOne/data/vlearn-pack"

# Mã đoạn trích dẫn trong transcript bản sạch: **[T04-064]**
PARA_CODE_RE = re.compile(r"\*\*\[(T\d{2}-\d{3})\]\*\*")
# Tiêu đề buổi nằm ở dòng H1 đầu file
SESSION_TITLE_RE = re.compile(r"^# Transcript bài giảng \(bản sạch\) — (.+)$", re.M)


def data_dir() -> Path:
    """Thư mục data pack. Báo lỗi rõ ràng thay vì crash mơ hồ ở tầng dưới."""
    raw = os.environ.get("VLEARN_DATA_DIR", DEFAULT_DATA_DIR)
    path = Path(raw)
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    if not path.is_dir():
        sys.exit(
            f"Không tìm thấy data pack tại {path}\n"
            f"Đặt VLEARN_DATA_DIR trỏ về thư mục vlearn-pack (xem .env.example)."
        )
    return path


@dataclass(frozen=True)
class Paragraph:
    """Một đoạn lời giảng có mã trích dẫn."""

    code: str  # T04-064
    text: str
    session: str  # "Day 1 — Foundation: cách LLM hoạt động (...)"
    source_file: str


def load_paragraphs() -> list[Paragraph]:
    """~700 đoạn từ 6 transcript bản sạch, giữ nguyên thứ tự file."""
    out: list[Paragraph] = []
    folder = data_dir() / "transcript"
    for path in sorted(folder.glob("transcript-*-clean.md")):
        raw = path.read_text(encoding="utf-8")
        title_match = SESSION_TITLE_RE.search(raw)
        session = title_match.group(1).strip() if title_match else path.stem

        marks = list(PARA_CODE_RE.finditer(raw))
        for i, mark in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(raw)
            body = raw[mark.end() : end].strip()
            # Bỏ heading markdown lẫn vào phần đuôi đoạn
            body = re.sub(r"\n#{1,6} .*$", "", body).strip()
            if body:
                out.append(Paragraph(mark.group(1), body, session, path.name))
    if not out:
        sys.exit(f"Không parse được đoạn nào trong {folder} — kiểm tra lại data pack.")
    return out


def load_chatlog() -> list[dict]:
    """2.522 dòng hội thoại thật (đã ẩn danh) — chỉ dùng để mining evidence."""
    path = data_dir() / "chatlog" / "chat_history_anonymized_for_hackathon.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_turns() -> dict[str, dict[str, dict]]:
    """Gom chatlog theo turn: {turn_id: {"student": row, "tutor": row}}."""
    turns: dict[str, dict[str, dict]] = {}
    for row in load_chatlog():
        turns.setdefault(row["turn_id"], {})[row["role"]] = row
    return turns
