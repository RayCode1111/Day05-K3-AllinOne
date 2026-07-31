"""Kho thông báo Discord của Nova: data pack tĩnh + thông báo đẩy lên lúc chạy.

Nova đọc hai kênh Discord của khoá học. Phần lịch sử nằm trong data pack
(`data/discord-pack/*.txt`, chỉ đọc, không sửa). Phần phát sinh — LabCoach đăng
tài liệu, BTC đẩy thông báo mới — được ghi vào `store/discord_inbox.json` để
lần quét kế tiếp Gemini có thêm dữ kiện.

Cả hai nguồn đi qua đây và ra cùng một hình dạng, nên tầng trên (agent, app)
không cần biết một thông báo đến từ file hay từ cửa sổ mô phỏng.
"""

from __future__ import annotations

import json
import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACK_DIR = ROOT / "data" / "discord-pack"
STORE_PATH = Path(__file__).resolve().parent / "store" / "discord_inbox.json"

# Mỗi file export ứng với một kênh Discord. Tên kênh là thứ hiển thị cho người
# dùng và đưa vào prompt, còn `id` dùng làm tiền tố cho source_id (bền hơn tên
# file có dấu cách).
CHANNELS = [
    {"id": "thong-bao-chung", "name": "Thông báo chung", "file": "discord notification.txt"},
    {"id": "thong-bao", "name": "Thông báo", "file": "discord notification v2.txt"},
]
CHANNEL_BY_ID = {channel["id"]: channel for channel in CHANNELS}

# Trong pack, hai thông báo khác nhau luôn cách nhau từ 2 dòng trống trở lên,
# còn xuống đoạn trong cùng một thông báo chỉ cách 1 dòng trống.
BLOCK_SPLIT = re.compile(r"\n\s*\n\s*\n+")
BLOCK_HEADER = re.compile(r"^---\s*\n\s*date:\s*(?P<date>[^\n]+)\n\s*message:\s*\|\s*\n(?P<body>.+)$", re.S)

PACK_AUTHOR = "LabCoach / BTC"


def _parse_block(raw: str) -> tuple[str, str]:
    """Bóc `date:` và thân `message:` ra khỏi block YAML-ish của pack."""
    match = BLOCK_HEADER.match(raw.strip())
    if not match:
        return "", raw.strip()
    return match.group("date").strip(), textwrap.dedent(match.group("body")).strip()


def pack_messages() -> list[dict]:
    """Thông báo lịch sử đọc từ data pack. Chỉ đọc, không bao giờ ghi đè."""
    messages: list[dict] = []
    for channel in CHANNELS:
        path = PACK_DIR / channel["file"]
        if not path.exists():
            continue
        blocks = [item for item in BLOCK_SPLIT.split(path.read_text(encoding="utf-8-sig").strip()) if item.strip()]
        for index, block in enumerate(blocks, start=1):
            posted_at, text = _parse_block(block)
            messages.append({
                "id": f"{channel['id']}#{index}",
                "channel_id": channel["id"],
                "channel": channel["name"],
                "author": PACK_AUTHOR,
                "date": posted_at,
                "text": text,
                "origin": "pack",
            })
    return messages


def _read_store() -> list[dict]:
    if not STORE_PATH.exists():
        return []
    try:
        data = json.loads(STORE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:  # file hỏng thì coi như kho rỗng, không làm sập app
        return []
    return data if isinstance(data, list) else []


def _write_store(messages: list[dict]) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8")


def inbox_messages() -> list[dict]:
    """Thông báo đã được đẩy lên trong lúc chạy, cũ trước mới sau."""
    return [item for item in _read_store() if item.get("channel_id") in CHANNEL_BY_ID]


def all_messages() -> list[dict]:
    """Toàn bộ dữ liệu Nova được phép đọc, gom theo kênh."""
    merged = pack_messages() + inbox_messages()
    order = {channel["id"]: index for index, channel in enumerate(CHANNELS)}
    return sorted(merged, key=lambda item: (order[item["channel_id"]], item["origin"] != "pack"))


def messages_of(channel_id: str) -> list[dict]:
    return [item for item in all_messages() if item["channel_id"] == channel_id]


def add_message(channel_id: str, author: str, text: str, posted_at: str) -> dict:
    """Ghi một thông báo mô phỏng vào kho. Trả về bản ghi vừa tạo."""
    if channel_id not in CHANNEL_BY_ID:
        raise ValueError(f"Kênh không hợp lệ: {channel_id}")
    if not text.strip():
        raise ValueError("Nội dung thông báo không được rỗng.")
    stored = _read_store()
    taken = {item.get("id") for item in stored}
    index = len(stored) + 1
    while f"{channel_id}#new-{index}" in taken:
        index += 1
    message = {
        "id": f"{channel_id}#new-{index}",
        "channel_id": channel_id,
        "channel": CHANNEL_BY_ID[channel_id]["name"],
        "author": author.strip() or PACK_AUTHOR,
        "date": posted_at,
        "text": text.strip(),
        "origin": "inbox",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    stored.append(message)
    _write_store(stored)
    return message


def delete_message(message_id: str) -> None:
    """Chỉ xoá được thông báo mô phỏng — data pack là bất biến."""
    _write_store([item for item in _read_store() if item.get("id") != message_id])


def clear_inbox() -> None:
    _write_store([])
