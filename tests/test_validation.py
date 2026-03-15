"""
Tests for the shared validation helpers used by flight logic.
"""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from record.validation import (
    airline_exists,
    client_exists,
    flight_exists,
    normalise_flight_record,
    same_flight,
    validate_date_string,
)


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.records = [
            {
                "ID": 1,
                "Type": "client",
                "Name": "John Smith",
                "Address Line 1": "12 Main Street",
                "Address Line 2": "",
                "Address Line 3": "",
                "City": "London",
                "State": "London",
                "Zip Code": "SW1A 1AA",
                "Country": "UK",
                "Phone Number": "07123456789",
            },
            {
                "ID": 10,
                "Type": "airline",
                "Company Name": "Emirates",
            },
        ]

    def test_validate_date_string_success(self):
        self.assertEqual(validate_date_string("2026-03-20 14:30"), "2026-03-20 14:30")

    def test_validate_date_string_failure(self):
        with self.assertRaises(ValueError):
            validate_date_string("20/03/2026")

    def test_client_exists(self):
        self.assertTrue(client_exists(self.records, 1))
        self.assertFalse(client_exists(self.records, 999))

    def test_airline_exists(self):
        self.assertTrue(airline_exists(self.records, 10))
        self.assertFalse(airline_exists(self.records, 999))

    def test_normalise_flight_record_success(self):
        flight = {
            "Client_ID": 1,
            "Airline_ID": 10,
            "Date": "2026-03-20 14:30",
            "Start City": "London",
            "End City": "Dubai",
        }

        result = normalise_flight_record(flight, self.records)
        self.assertEqual(result["Type"], "flight")
        self.assertEqual(result["Client_ID"], 1)
        self.assertEqual(result["Airline_ID"], 10)

    def test_normalise_flight_record_invalid_client(self):
        flight = {
            "Client_ID": 999,
            "Airline_ID": 10,
            "Date": "2026-03-20 14:30",
            "Start City": "London",
            "End City": "Dubai",
        }

        with self.assertRaises(ValueError):
            normalise_flight_record(flight, self.records)

    def test_normalise_flight_record_invalid_airline(self):
        flight = {
            "Client_ID": 1,
            "Airline_ID": 999,
            "Date": "2026-03-20 14:30",
            "Start City": "London",
            "End City": "Dubai",
        }

        with self.assertRaises(ValueError):
            normalise_flight_record(flight, self.records)

    def test_same_flight(self):
        a = {
            "Client_ID": 1,
            "Airline_ID": 10,
            "Date": "2026-03-20 14:30",
            "Start City": "London",
            "End City": "Dubai",
        }
        b = {
            "Client_ID": 1,
            "Airline_ID": 10,
            "Date": "2026-03-20 14:30",
            "Start City": "London",
            "End City": "Dubai",
        }
        self.assertTrue(same_flight(a, b))

    def test_flight_exists(self):
        existing = {
            "Type": "flight",
            "Client_ID": 1,
            "Airline_ID": 10,
            "Date": "2026-03-20 14:30",
            "Start City": "London",
            "End City": "Dubai",
        }
        self.records.append(existing)

        candidate = {
            "Type": "flight",
            "Client_ID": 1,
            "Airline_ID": 10,
            "Date": "2026-03-20 14:30",
            "Start City": "London",
            "End City": "Dubai",
        }

        self.assertTrue(flight_exists(self.records, candidate))


if __name__ == "__main__":
    unittest.main()
