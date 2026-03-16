"""
This is my part of the project (Member 3). It handles saving and loading
the records to a JSONL file.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import jsonlines

# Figuring out the project root so we can have a stable path to the records file.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RECORD_PATH = PROJECT_ROOT / "src" / "record" / "record.jsonl"
RECORD_PATH_ENV_VAR = "RMS_RECORD_PATH" # an env var to override the path for testing


def resolve_record_path(path: Path | str | None = None) -> Path:
    """Finds the right path for the records file. Order of priority:
    1. An explicit path passed to the function
    2. The environment variable
    3. The default path
    """
    if path is not None:
        return Path(path)

    env_path = os.getenv(RECORD_PATH_ENV_VAR)
    if env_path:
        return Path(env_path)

    return DEFAULT_RECORD_PATH


def ensure_record_file(path: Path | str | None = None) -> Path:
    """Just makes sure the parent directory for the records file exists."""
    resolved_path = resolve_record_path(path)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    return resolved_path


def load_records(path: Path | str | None = None) -> list[dict[str, Any]]:
    """Loads records from the JSONL file.

    I made this super defensive. If the file is missing, empty, or has garbage in it,
    it will just return an empty list so the app doesn't crash on startup.
    """
    resolved_path = ensure_record_file(path)

    if not resolved_path.exists() or resolved_path.stat().st_size == 0:
        return [] # Nothing to do here

    records: list[dict[str, Any]] = []
    try:
        with jsonlines.open(resolved_path, mode="r") as reader:
            for obj in reader:
                # Make sure we only add dictionaries to our list
                if isinstance(obj, dict):
                    records.append(obj)
    except (jsonlines.InvalidLineError, UnicodeDecodeError, OSError):
        # Something is wrong with the file, better to start fresh than crash.
        return []

    return records


def save_records(records: list[dict[str, Any]], path: Path | str | None = None) -> None:
    """Saves the whole list of records back to the JSONL file."""
    if not isinstance(records, list):
        raise ValueError("Hey, records needs to be a list of dictionaries!")

    # A quick check to make sure we're not writing garbage
    if any(not isinstance(record, dict) for record in records):
        raise ValueError("Each record in the list has to be a dictionary.")

    resolved_path = ensure_record_file(path)
    with jsonlines.open(resolved_path, mode="w") as writer:
        writer.write_all(records)


def close_application(records: list[dict[str, Any]], root, path: Path | str | None = None) -> None:
    """Saves the records and then closes the GUI.

    Important: the root window is only destroyed if the save is successful.
    """
    save_records(records, path)
    root.destroy()
