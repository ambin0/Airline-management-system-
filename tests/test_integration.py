"""Integration-style tests for storage and shutdown flow."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data.storage import close_application, load_records


class MockRoot:
    def __init__(self):
        self.destroy_called = False

    def destroy(self):
        self.destroy_called = True


class TestStorageIntegration(unittest.TestCase):
    def test_records_persist_between_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "records.jsonl"
            records = [
                {"ID": 1, "Type": "client", "Name": "Fatima"},
                {"ID": 10, "Type": "airline", "Company Name": "Emirates"},
                {
                    "Client_ID": 1,
                    "Airline_ID": 10,
                    "Date": "2026-04-01 09:00",
                    "Start City": "Dubai",
                    "End City": "Amman",
                    "Type": "flight",
                },
            ]
            root = MockRoot()

            close_application(records, root, path)

            self.assertTrue(root.destroy_called)
            self.assertEqual(load_records(path), records)

    def test_close_application_does_not_destroy_root_when_save_fails(self):
        root = MockRoot()

        with self.assertRaises(ValueError):
            close_application("not-a-list", root)

        self.assertFalse(root.destroy_called)


if __name__ == "__main__":
    unittest.main()
