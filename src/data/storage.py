from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonlines


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RECORD_PATH = PROJECT_ROOT / "src" / "record" / "record.jsonl"


def ensure_record_file(path: Path = DEFAULT_RECORD_PATH) -> None:
    """Ensure the parent directory and JSONL file exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()


def load_records(path: Path = DEFAULT_RECORD_PATH) -> list[dict[str, Any]]:
    """Load all records from the JSONL file into a list of dictionaries."""
    ensure_record_file(path)

    if path.stat().st_size == 0:
        return []

    records: list[dict[str, Any]] = []
    with jsonlines.open(path, mode="r") as reader:
        for obj in reader:
            if isinstance(obj, dict):
                records.append(obj)
    return records


def save_records(records: list[dict[str, Any]], path: Path = DEFAULT_RECORD_PATH) -> None:
    """Save the full in-memory records list to the JSONL file."""
    ensure_record_file(path)
    with jsonlines.open(path, mode="w") as writer:
        writer.write_all(records)


def close_application(records: list[dict[str, Any]], root, path: Path = DEFAULT_RECORD_PATH) -> None:
    """Save records, then close the GUI application."""
    save_records(records, path)
    root.destroy()
