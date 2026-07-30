"""OBSERVE — nạp tin nhắn Discord trong ngày.

Corpus là DATA GIẢ TỰ SINH (xem `_meta.vi_sao` trong từng file fixtures).
Hướng B không có data pack; đề bài cho phép data giả tự sinh.
"""

from __future__ import annotations

import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"

BO_CORPUS = {
    "ngay-thuong": FIXTURES / "discord_day_mock.json",
    "tin-hiem": FIXTURES / "discord_edge_cases.json",
}


def nap(ten: str) -> tuple[list[dict], dict]:
    """Trả về (messages, meta). `ten` là khoá trong BO_CORPUS."""
    path = BO_CORPUS.get(ten)
    if path is None:
        raise KeyError(f"Corpus không tồn tại: {ten}. Có: {', '.join(BO_CORPUS)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["messages"], data["_meta"]


def nap_tat_ca() -> dict[str, tuple[list[dict], dict]]:
    return {ten: nap(ten) for ten in BO_CORPUS}


def tin_theo_id() -> dict[str, dict]:
    """Tra ngược một tin bất kỳ theo id, không cần biết nó ở corpus nào."""
    out: dict[str, dict] = {}
    for ten in BO_CORPUS:
        messages, _ = nap(ten)
        for m in messages:
            out[m["id"]] = {**m, "_corpus": ten}
    return out
