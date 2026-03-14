"""
Tests for the client CRUD functions.
"""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from record.client_crud import (
    create_client,
    delete_client,
    get_client_by_id,
    search_clients_by_name,
    update_client,
)


class TestClientCrud(unittest.TestCase):
    def setUp(self):
        """Reset the records list for each test to keep them independent."""
        self.records = []

    def test_create_client_works(self):
        client = create_client(
            self.records,
            {
                "ID": 1,
                "Name": "John Smith",
                "City": "London",
                "Country": "UK",
            },
        )
        self.assertEqual(client["ID"], 1)
        self.assertEqual(client["Type"], "client")
        self.assertEqual(len(self.records), 1)

    def test_create_client_no_duplicate_ids(self):
        create_client(self.records, {"ID": 1, "Name": "John Smith"})
        with self.assertRaises(ValueError):
            create_client(self.records, {"ID": 1, "Name": "Another John"})

    def test_create_client_needs_name(self):
        with self.assertRaises(ValueError):
            create_client(self.records, {"ID": 1}) # Missing the Name field

    def test_get_client_by_id_found(self):
        create_client(self.records, {"ID": 1, "Name": "John Smith"})
        client = get_client_by_id(self.records, 1)
        self.assertIsNotNone(client)
        self.assertEqual(client["Name"], "John Smith")

    def test_get_client_by_id_not_found(self):
        client = get_client_by_id(self.records, 99)
        self.assertIsNone(client)

    def test_search_clients_by_name_is_case_insensitive(self):
        create_client(self.records, {"ID": 1, "Name": "John Smith"})
        create_client(self.records, {"ID": 2, "Name": "Johnny Doe"})
        create_client(self.records, {"ID": 3, "Name": "Alice Brown"})

        results = search_clients_by_name(self.records, "john")
        self.assertEqual(len(results), 2)

    def test_update_client_works(self):
        create_client(self.records, {"ID": 1, "Name": "John Smith"})
        updated = update_client(self.records, 1, {"Phone Number": "123456", "City": "London"})
        self.assertIsNotNone(updated)
        self.assertEqual(updated["Phone Number"], "123456")
        self.assertEqual(updated["City"], "London")

    def test_update_client_doesnt_change_protected_fields(self):
        create_client(self.records, {"ID": 1, "Name": "John Smith"})
        # Trying to change ID and Type should be blocked
        updated = update_client(self.records, 1, {"ID": 99, "Type": "airline", "Name": "John Updated"})
        self.assertEqual(updated["ID"], 1)
        self.assertEqual(updated["Type"], "client")
        self.assertEqual(updated["Name"], "John Updated")

    def test_update_client_returns_none_if_not_found(self):
        updated = update_client(self.records, 99, {"City": "Paris"})
        self.assertIsNone(updated)

    def test_delete_client_works(self):
        create_client(self.records, {"ID": 1, "Name": "John Smith"})
        result = delete_client(self.records, 1)
        self.assertTrue(result)
        self.assertEqual(len(self.records), 0)

    def test_delete_client_returns_false_if_not_found(self):
        result = delete_client(self.records, 99)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
