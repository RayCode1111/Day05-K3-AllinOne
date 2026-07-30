"""Nạp data pack Discord từ đường dẫn cấu hình bằng biến môi trường.

Data pack KHÔNG nằm trong repo này (luật bảo mật: không commit data pack vào
repo nộp bài — `.gitignore` chặn `data/`). Mọi module khác đi qua đây để lấy
đường dẫn, không hardcode.

Pack là text thô, không có metadata từng tin (`ts`, `tac_gia`, `vai`). Vì thế
pack chỉ dùng để **đếm bằng chứng** trong `evidence.py`, KHÔNG dùng làm corpus
cho eval — lý do đầy đủ ở spec.md §7.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

try:  # .env là tuỳ chọn — chạy được cả khi export biến môi trường bằng tay
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:  # pragma: no cover
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = "../Day05-K3-AllinOne/data/discord-pack"

# Ranh giới giữa hai thông báo. Trong pack, xuống đoạn TRONG một thông báo chỉ
# cách nhau đúng 1 dòng trống (\n\n — 114 lần), còn giữa hai thông báo khác nhau
# luôn cách từ 2 dòng trống trở lên (\n\n\n+ — 25 lần). Ngưỡng >=3 newline vì thế
# tách đúng tin, không cắt vụn một tin dài thành nhiều mảnh.
RANH_GIOI_TIN = re.compile(r"\n{3,}")


def data_dir() -> Path:
    """Thư mục data pack. Báo lỗi rõ ràng thay vì crash mơ hồ ở tầng dưới."""
    raw = os.environ.get("DISCORD_DATA_DIR", DEFAULT_DATA_DIR)
    path = Path(raw)
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    if not path.is_dir():
        sys.exit(
            f"Không tìm thấy data pack tại {path}\n"
            f"Đặt DISCORD_DATA_DIR trỏ về thư mục discord-pack (xem .env.example)."
        )
    return path


def load_messages() -> list[str]:
    """Trả về danh sách thông báo, đã tách theo ranh giới tin và bỏ tin rỗng."""
    tin: list[str] = []
    for path in sorted(data_dir().glob("*.txt")):
        noi_dung = path.read_text(encoding="utf-8")
        tin += [k.strip() for k in RANH_GIOI_TIN.split(noi_dung) if k.strip()]
    return tin
