"""
Tests for the flight CRUD functions. This one is important because
flights don't have a simple ID, so matching them is a bit complex.
"""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from record.flight_crud import (
    build_flight_key,
    create_flight,
    delete_flight,
    get_all_flights,
    search_flights,
    update_flight,
)


class TestFlightCrud(unittest.TestCase):
    def setUp(self):
        """Set up a clean list of records for each test."""
        self.records = []

        # Some test data to reuse
        self.flight_1 = {
            "Client_ID": 1,
            "Airline_ID": 10,
            "Date": "2026-03-20 10:00",
            "Start City": "Dubai",
            "End City": "London",
        }

        self.flight_2 = {
            "Client_ID": 2,
            "Airline_ID": 11,
            "Date": "2026-03-21 12:00",
            "Start City": "Abu Dhabi",
            "End City": "Paris",
        }

    def test_build_flight_key(self):
        """Just check that the key builder works as expected."""
        key = build_flight_key(self.flight_1)
        self.assertEqual(key["Client_ID"], 1)
        self.assertEqual(key["Start City"], "Dubai")

    def test_create_flight_adds_record(self):
        flight = create_flight(self.records, self.flight_1)
        self.assertEqual(flight["Type"], "flight")
        self.assertEqual(len(self.records), 1)

    def test_create_flight_rejects_missing_fields(self):
        with self.assertRaises(ValueError):
            # This is missing a bunch of required stuff
            create_flight(self.records, {"Client_ID": 1, "Airline_ID": 10})

    def test_create_flight_rejects_duplicates(self):
        create_flight(self.records, self.flight_1)
        # Trying to add the exact same flight again should fail
        with self.assertRaises(ValueError):
            create_flight(self.records, self.flight_1)

    def test_get_all_flights(self):
        create_flight(self.records, self.flight_1)
        create_flight(self.records, self.flight_2)
        flights = get_all_flights(self.records)
        self.assertEqual(len(flights), 2)

    def test_search_flights_by_client(self):
        create_flight(self.records, self.flight_1)
        create_flight(self.records, self.flight_2)

        results = search_flights(self.records, {"Client_ID": 1})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["End City"], "London")

    def test_search_flights_by_route(self):
        create_flight(self.records, self.flight_1)
        results = search_flights(self.records, {"Start City": "Dubai", "End City": "London"})
        self.assertEqual(len(results), 1)

    def test_update_flight_works(self):
        create_flight(self.records, self.flight_1)

        updated = update_flight(
            self.records,
            build_flight_key(self.flight_1),
            {"End City": "Manchester"}, # Changing the destination
        )

        self.assertIsNotNone(updated)
        self.assertEqual(updated["End City"], "Manchester")

    def test_update_flight_returns_none_if_not_found(self):
        updated = update_flight(self.records, {"Client_ID": 99}, {"End City": "Rome"})
        self.assertIsNone(updated)

    def test_update_flight_doesnt_change_type(self):
        create_flight(self.records, self.flight_1)

        updated = update_flight(
            self.records,
            build_flight_key(self.flight_1),
            {"Type": "client", "End City": "Manchester"}, # Sneaky!
        )

        self.assertEqual(updated["Type"], "flight")
        self.assertEqual(updated["End City"], "Manchester")

    def test_update_flight_raises_error_if_not_unique(self):
        create_flight(self.records, self.flight_1)
        # A second flight for the same client
        create_flight(self.records, {
            "Client_ID": 1,
            "Airline_ID": 12,
            "Date": "2026-03-25 15:00",
            "Start City": "Dubai",
            "End City": "Rome",
        })

        # This is too vague, should raise an error
        with self.assertRaises(ValueError):
            update_flight(self.records, {"Client_ID": 1}, {"End City": "Milan"})

    def test_delete_flight_works(self):
        create_flight(self.records, self.flight_1)
        result = delete_flight(self.records, build_flight_key(self.flight_1))
        self.assertTrue(result)
        self.assertEqual(len(self.records), 0)

    def test_delete_flight_returns_false_if_not_found(self):
        result = delete_flight(self.records, {"Client_ID": 99})
        self.assertFalse(result)

    def test_delete_flight_raises_error_if_not_unique(self):
        create_flight(self.records, self.flight_1)
        create_flight(self.records, {
            "Client_ID": 1,
            "Airline_ID": 12,
            "Date": "2026-03-25 15:00",
            "Start City": "Dubai",
            "End City": "Rome",
        })

        # Too vague, should fail
        with self.assertRaises(ValueError):
            delete_flight(self.records, {"Client_ID": 1})


if __name__ == "__main__":
    unittest.main()
