from __future__ import annotations

from datetime import datetime
from typing import Any


DATE_FORMAT = "%Y-%m-%d %H:%M"


def require_field(record: dict[str, Any], field_name: str) -> Any:
    """Return a required field value or raise an error if missing."""
    if field_name not in record:
        raise ValueError(f"Missing field: {field_name}")
    return record[field_name]


def require_non_empty_string(record: dict[str, Any], field_name: str) -> str:
    """Return a required non-empty string value."""
    value = require_field(record, field_name)
    value = str(value).strip()
    if value == "":
        raise ValueError(f"{field_name} cannot be empty.")
    return value


def require_int(record: dict[str, Any], field_name: str) -> int:
    """Return a required integer value."""
    value = require_field(record, field_name)
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be an integer.") from None


def validate_date_string(date_str: str) -> str:
    """Validate the agreed flight date format."""
    try:
        datetime.strptime(date_str, DATE_FORMAT)
    except ValueError as exc:
        raise ValueError(f"Date must be in format {DATE_FORMAT}.") from exc
    return date_str


def client_exists(records: list[dict[str, Any]], client_id: int) -> bool:
    """Check whether a client exists by ID."""
    return any(
        record.get("Type") == "client" and record.get("ID") == client_id
        for record in records
    )


def airline_exists(records: list[dict[str, Any]], airline_id: int) -> bool:
    """Check whether an airline exists by ID."""
    return any(
        record.get("Type") == "airline" and record.get("ID") == airline_id
        for record in records
    )


def normalise_flight_record(
    flight_data: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate and normalise a flight record."""
    client_id = require_int(flight_data, "Client_ID")
    airline_id = require_int(flight_data, "Airline_ID")
    date_value = require_non_empty_string(flight_data, "Date")
    start_city = require_non_empty_string(flight_data, "Start City")
    end_city = require_non_empty_string(flight_data, "End City")

    validate_date_string(date_value)

    if not client_exists(records, client_id):
        raise ValueError("Client_ID does not exist.")

    if not airline_exists(records, airline_id):
        raise ValueError("Airline_ID does not exist.")

    return {
        "Type": "flight",
        "Client_ID": client_id,
        "Airline_ID": airline_id,
        "Date": date_value,
        "Start City": start_city,
        "End City": end_city,
    }


def same_flight(record_a: dict[str, Any], record_b: dict[str, Any]) -> bool:
    """Compare flights using the agreed composite identity."""
    return (
        record_a.get("Client_ID") == record_b.get("Client_ID")
        and record_a.get("Airline_ID") == record_b.get("Airline_ID")
        and record_a.get("Date") == record_b.get("Date")
        and record_a.get("Start City") == record_b.get("Start City")
        and record_a.get("End City") == record_b.get("End City")
    )


def flight_exists(records: list[dict[str, Any]], flight_record: dict[str, Any]) -> bool:
    """Check whether an identical flight already exists."""
    return any(
        record.get("Type") == "flight" and same_flight(record, flight_record)
        for record in records
    )
