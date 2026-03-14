"""
Tests for the airline CRUD functions.
"""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from record.airline_crud import (
    create_airline,
    delete_airline,
    get_airline_by_id,
    search_airlines_by_name,
    update_airline,
)


class TestAirlineCrud(unittest.TestCase):
    def setUp(self):
        """Wipe the records list before each test."""
        self.records = []

    def test_create_airline(self):
        airline = create_airline(
            self.records,
            {"ID": 10, "Company Name": "Emirates"},
        )
        self.assertEqual(airline["ID"], 10)
        self.assertEqual(airline["Type"], "airline")
        self.assertEqual(len(self.records), 1)

    def test_create_airline_rejects_duplicate_id(self):
        create_airline(self.records, {"ID": 10, "Company Name": "Emirates"})
        # now try to add another one with the same ID
        with self.assertRaises(ValueError):
            create_airline(self.records, {"ID": 10, "Company Name": "Qatar Airways"})

    def test_create_airline_needs_required_fields(self):
        with self.assertRaises(ValueError):
            create_airline(self.records, {"ID": 10}) # Missing company name

    def test_get_airline_by_id_finds_it(self):
        create_airline(self.records, {"ID": 10, "Company Name": "Emirates"})
        airline = get_airline_by_id(self.records, 10)
        self.assertIsNotNone(airline)
        self.assertEqual(airline["Company Name"], "Emirates")

    def test_get_airline_by_id_returns_none_if_missing(self):
        airline = get_airline_by_id(self.records, 99)
        self.assertIsNone(airline)

    def test_search_airlines_by_name(self):
        create_airline(self.records, {"ID": 10, "Company Name": "Emirates"})
        create_airline(self.records, {"ID": 11, "Company Name": "Emirates SkyCargo"})
        create_airline(self.records, {"ID": 12, "Company Name": "Etihad"})

        # search should be case-insensitive
        results = search_airlines_by_name(self.records, "emirates")
        self.assertEqual(len(results), 2)

    def test_update_airline_works(self):
        create_airline(self.records, {"ID": 10, "Company Name": "Emirates"})
        updated = update_airline(self.records, 10, {"Company Name": "Emirates Airline"})
        self.assertIsNotNone(updated)
        self.assertEqual(updated["Company Name"], "Emirates Airline")

    def test_update_airline_doesnt_change_protected_fields(self):
        create_airline(self.records, {"ID": 10, "Company Name": "Emirates"})
        # try to change the ID and Type, it shouldn't work
        updated = update_airline(self.records, 10, {"ID": 99, "Type": "client", "Company Name": "Updated"})
        self.assertEqual(updated["ID"], 10)
        self.assertEqual(updated["Type"], "airline")
        self.assertEqual(updated["Company Name"], "Updated")

    def test_update_airline_returns_none_if_missing(self):
        updated = update_airline(self.records, 99, {"Company Name": "Unknown"})
        self.assertIsNone(updated)

    def test_delete_airline_works(self):
        create_airline(self.records, {"ID": 10, "Company Name": "Emirates"})
        result = delete_airline(self.records, 10)
        self.assertTrue(result)
        self.assertEqual(len(self.records), 0)

    def test_delete_airline_returns_false_if_missing(self):
        result = delete_airline(self.records, 99)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
