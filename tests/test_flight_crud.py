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
        self.records = [
            {
                "ID": 1,
                "Type": "client",
                "Name": "Client One",
                "Address Line 1": "1 Main Street",
                "Address Line 2": "",
                "Address Line 3": "",
                "City": "Dubai",
                "State": "Dubai",
                "Zip Code": "00001",
                "Country": "UAE",
                "Phone Number": "0700000001",
            },
            {
                "ID": 2,
                "Type": "client",
                "Name": "Client Two",
                "Address Line 1": "2 Main Street",
                "Address Line 2": "",
                "Address Line 3": "",
                "City": "Abu Dhabi",
                "State": "Abu Dhabi",
                "Zip Code": "00002",
                "Country": "UAE",
                "Phone Number": "0700000002",
            },
            {
                "ID": 10,
                "Type": "airline",
                "Company Name": "Emirates",
            },
            {
                "ID": 11,
                "Type": "airline",
                "Company Name": "Qatar Airways",
            },
            {
                "ID": 12,
                "Type": "airline",
                "Company Name": "Etihad",
            },
        ]

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
        self.assertEqual(len(get_all_flights(self.records)), 1)

    def test_create_flight_rejects_missing_fields(self):
        with self.assertRaises(ValueError):
            create_flight(self.records, {"Client_ID": 1, "Airline_ID": 10})

    def test_create_flight_rejects_duplicates(self):
        create_flight(self.records, self.flight_1)
        with self.assertRaises(ValueError):
            create_flight(self.records, self.flight_1)

    def test_create_flight_rejects_invalid_client(self):
        invalid_flight = {
            "Client_ID": 999,
            "Airline_ID": 10,
            "Date": "2026-03-22 09:00",
            "Start City": "Dubai",
            "End City": "Berlin",
        }
        with self.assertRaises(ValueError):
            create_flight(self.records, invalid_flight)

    def test_create_flight_rejects_invalid_airline(self):
        invalid_flight = {
            "Client_ID": 1,
            "Airline_ID": 999,
            "Date": "2026-03-22 09:00",
            "Start City": "Dubai",
            "End City": "Berlin",
        }
        with self.assertRaises(ValueError):
            create_flight(self.records, invalid_flight)

    def test_create_flight_rejects_invalid_date(self):
        invalid_flight = {
            "Client_ID": 1,
            "Airline_ID": 10,
            "Date": "22/03/2026",
            "Start City": "Dubai",
            "End City": "Berlin",
        }
        with self.assertRaises(ValueError):
            create_flight(self.records, invalid_flight)

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
            {"End City": "Manchester"},
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
            {"Type": "client", "End City": "Manchester"},
        )

        self.assertEqual(updated["Type"], "flight")
        self.assertEqual(updated["End City"], "Manchester")

    def test_update_flight_raises_error_if_not_unique(self):
        create_flight(self.records, self.flight_1)
        create_flight(self.records, {
            "Client_ID": 1,
            "Airline_ID": 12,
            "Date": "2026-03-25 15:00",
            "Start City": "Dubai",
            "End City": "Rome",
        })

        with self.assertRaises(ValueError):
            update_flight(self.records, {"Client_ID": 1}, {"End City": "Milan"})

    def test_update_flight_rejects_duplicate_result(self):
        create_flight(self.records, self.flight_1)
        create_flight(self.records, {
            "Client_ID": 1,
            "Airline_ID": 10,
            "Date": "2026-03-21 10:00",
            "Start City": "Dubai",
            "End City": "Manchester",
        })

        with self.assertRaises(ValueError):
            update_flight(
                self.records,
                {
                    "Client_ID": 1,
                    "Airline_ID": 10,
                    "Date": "2026-03-21 10:00",
                    "Start City": "Dubai",
                    "End City": "Manchester",
                },
                {
                    "Date": "2026-03-20 10:00",
                    "Start City": "Dubai",
                    "End City": "London",
                },
            )

    def test_delete_flight_works(self):
        create_flight(self.records, self.flight_1)
        result = delete_flight(self.records, build_flight_key(self.flight_1))
        self.assertTrue(result)
        self.assertEqual(len(get_all_flights(self.records)), 0)

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

        with self.assertRaises(ValueError):
            delete_flight(self.records, {"Client_ID": 1})


if __name__ == "__main__":
    unittest.main()
