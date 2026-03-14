"""
Tests for the shared CRUD helper functions.
"""

from pathlib import Path
import sys
import unittest

# This is a bit of a hack to get the src folder into the python path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from record.crud_helpers import (
    delete_record_at_index,
    ensure_required_fields,
    find_record_index_by_id,
    find_records_by_criteria,
    find_records_by_field_contains,
    get_records_by_type,
    matches_criteria,
    record_exists_by_id,
    update_record_fields,
)


class TestCrudHelpers(unittest.TestCase):
    def setUp(self):
        """Create some dummy records for the tests to use."""
        self.records = [
            {"ID": 1, "Type": "client", "Name": "John Smith"},
            {"ID": 2, "Type": "client", "Name": "Alice Brown"},
            {"ID": 10, "Type": "airline", "Company Name": "Emirates"},
            {
                "Type": "flight",
                "Client_ID": 1,
                "Airline_ID": 10,
                "Date": "2026-03-20 10:00",
                "Start City": "Dubai",
                "End City": "London",
            },
        ]

    def test_ensure_required_fields_ok(self):
        # This should be fine
        ensure_required_fields({"ID": 1, "Name": "John"}, ["ID", "Name"])

    def test_ensure_required_fields_raises_on_missing(self):
        with self.assertRaises(ValueError):
            ensure_required_fields({"ID": 1}, ["ID", "Name"])

    def test_ensure_required_fields_raises_on_empty(self):
        with self.assertRaises(ValueError):
            ensure_required_fields({"ID": 1, "Name": ""}, ["ID", "Name"])

    def test_get_records_by_type(self):
        clients = get_records_by_type(self.records, "client")
        self.assertEqual(len(clients), 2)

    def test_find_record_index_by_id_found(self):
        index = find_record_index_by_id(self.records, "client", 1)
        self.assertEqual(index, 0)

    def test_find_record_index_by_id_not_found(self):
        index = find_record_index_by_id(self.records, "client", 99)
        self.assertEqual(index, -1)

    def test_record_exists_by_id_true(self):
        self.assertTrue(record_exists_by_id(self.records, "airline", 10))

    def test_record_exists_by_id_false(self):
        self.assertFalse(record_exists_by_id(self.records, "airline", 99))

    def test_update_record_fields(self):
        record = {"ID": 1, "Type": "client", "Name": "John"}
        updated = update_record_fields(record, {"Name": "Johnny", "City": "London"})
        self.assertEqual(updated["Name"], "Johnny")
        self.assertEqual(updated["City"], "London")

    def test_update_record_fields_blocked(self):
        record = {"ID": 1, "Type": "client", "Name": "John"}
        updated = update_record_fields(
            record,
            {"ID": 99, "Type": "airline", "Name": "Johnny"},
            blocked_fields=["ID", "Type"], # don't change these!
        )
        self.assertEqual(updated["ID"], 1)
        self.assertEqual(updated["Type"], "client")
        self.assertEqual(updated["Name"], "Johnny")

    def test_delete_record_at_index(self):
        result = delete_record_at_index(self.records, 0)
        self.assertTrue(result)
        self.assertEqual(len(self.records), 3)

    def test_delete_record_at_index_invalid(self):
        result = delete_record_at_index(self.records, 99)
        self.assertFalse(result)

    def test_find_records_by_field_contains_case_insensitive(self):
        results = find_records_by_field_contains(self.records, "client", "Name", "john")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["Name"], "John Smith")

    def test_matches_criteria_true(self):
        flight = self.records[3]
        self.assertTrue(matches_criteria(flight, {"Client_ID": 1, "Start City": "Dubai"}))

    def test_matches_criteria_false(self):
        flight = self.records[3]
        self.assertFalse(matches_criteria(flight, {"Client_ID": 2}))

    def test_find_records_by_criteria(self):
        results = find_records_by_criteria(
            self.records,
            "flight",
            {"Client_ID": 1, "Airline_ID": 10},
        )
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
