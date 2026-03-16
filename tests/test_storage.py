"""Tests for the storage layer."""

from pathlib import Path
import os
import sys
import tempfile
import unittest

import jsonlines

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data.storage import (
    RECORD_PATH_ENV_VAR,
    load_records,
    resolve_record_path,
    save_records,
)


class TestStorage(unittest.TestCase):
    def test_load_records_returns_empty_list_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "missing.jsonl"
            self.assertEqual(load_records(path), [])

    def test_load_records_returns_empty_list_when_file_empty(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "records.jsonl"
            path.touch()
            self.assertEqual(load_records(path), [])

    def test_load_records_ignores_non_dictionary_rows(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "records.jsonl"
            with jsonlines.open(path, mode="w") as writer:
                writer.write({"ID": 1, "Type": "client", "Name": "Amina"})
                writer.write(["not", "a", "dict"])
                writer.write("plain text")
                writer.write({"ID": 2, "Type": "airline", "Company Name": "Sky Gulf"})

            records = load_records(path)
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["Name"], "Amina")
            self.assertEqual(records[1]["Company Name"], "Sky Gulf")

    def test_load_records_returns_empty_list_when_file_is_invalid_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "records.jsonl"
            path.write_text('{"ID": 1}\n{bad json}\n', encoding="utf-8")
            self.assertEqual(load_records(path), [])

    def test_save_records_writes_jsonl_and_can_reload(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "records.jsonl"
            expected = [
                {"ID": 1, "Type": "client", "Name": "John Smith"},
                {"ID": 2, "Type": "airline", "Company Name": "Air Blue"},
            ]

            save_records(expected, path)
            actual = load_records(path)
            self.assertEqual(actual, expected)

    def test_save_records_rejects_non_list_input(self):
        with self.assertRaises(ValueError):
            save_records({"ID": 1})

    def test_save_records_rejects_non_dictionary_rows(self):
        with self.assertRaises(ValueError):
            save_records([{"ID": 1}, "bad row"])

    def test_resolve_record_path_uses_environment_variable(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = str(Path(tmp_dir) / "env_records.jsonl")
            original = os.environ.get(RECORD_PATH_ENV_VAR)
            os.environ[RECORD_PATH_ENV_VAR] = env_path
            try:
                self.assertEqual(resolve_record_path(), Path(env_path))
            finally:
                if original is None:
                    os.environ.pop(RECORD_PATH_ENV_VAR, None)
                else:
                    os.environ[RECORD_PATH_ENV_VAR] = original


if __name__ == "__main__":
    unittest.main()
