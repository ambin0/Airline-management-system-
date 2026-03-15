from __future__ import annotations

from datetime import datetime
from typing import Any


DATE_FORMAT = "%Y-%m-%d %H:%M"
VALID_RECORD_TYPES = {"client", "airline", "flight"}


def validate_record_type(record_type: str) -> str:
    """Validate that the record type is one of the allowed values."""
    if record_type not in VALID_RECORD_TYPES:
        raise ValueError("Type must be one of: client, airline, flight.")
    return record_type


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
    """Validate the date string against the agreed format."""
    try:
        datetime.strptime(date_str, DATE_FORMAT)
    except ValueError as exc:
        raise ValueError(f"Date must be in format {DATE_FORMAT}.") from exc
    return date_str


def client_exists(records: list[dict[str, Any]], client_id: int) -> bool:
    """Check whether a client record exists by ID."""
    return any(
        record.get("Type") == "client" and record.get("ID") == client_id
        for record in records
    )


def airline_exists(records: list[dict[str, Any]], airline_id: int) -> bool:
    """Check whether an airline record exists by ID."""
    return any(
        record.get("Type") == "airline" and record.get("ID") == airline_id
        for record in records
    )


def normalise_client_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalise a client record."""
    normalised = {
        "ID": require_int(record, "ID"),
        "Type": "client",
        "Name": require_non_empty_string(record, "Name"),
        "Address Line 1": str(record.get("Address Line 1", "")).strip(),
        "Address Line 2": str(record.get("Address Line 2", "")).strip(),
        "Address Line 3": str(record.get("Address Line 3", "")).strip(),
        "City": require_non_empty_string(record, "City"),
        "State": require_non_empty_string(record, "State"),
        "Zip Code": require_non_empty_string(record, "Zip Code"),
        "Country": require_non_empty_string(record, "Country"),
        "Phone Number": require_non_empty_string(record, "Phone Number"),
    }
    return normalised


def normalise_airline_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalise an airline record."""
    normalised = {
        "ID": require_int(record, "ID"),
        "Type": "airline",
        "Company Name": require_non_empty_string(record, "Company Name"),
    }
    return normalised


def normalise_flight_record(
    record: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate and normalise a flight record."""
    client_id = require_int(record, "Client_ID")
    airline_id = require_int(record, "Airline_ID")
    date_str = require_non_empty_string(record, "Date")
    start_city = require_non_empty_string(record, "Start City")
    end_city = require_non_empty_string(record, "End City")

    validate_date_string(date_str)

    if not client_exists(records, client_id):
        raise ValueError("Client_ID does not exist.")

    if not airline_exists(records, airline_id):
        raise ValueError("Airline_ID does not exist.")

    normalised = {
        "Type": "flight",
        "Client_ID": client_id,
        "Airline_ID": airline_id,
        "Date": date_str,
        "Start City": start_city,
        "End City": end_city,
    }
    return normalised


def same_flight(record_a: dict[str, Any], record_b: dict[str, Any]) -> bool:
    """
    Compare flights using the team's agreed composite identity:
    Client_ID + Airline_ID + Date + Start City + End City
    """
    return (
        record_a.get("Client_ID") == record_b.get("Client_ID")
        and record_a.get("Airline_ID") == record_b.get("Airline_ID")
        and record_a.get("Date") == record_b.get("Date")
        and record_a.get("Start City") == record_b.get("Start City")
        and record_a.get("End City") == record_b.get("End City")
    )


def flight_exists(records: list[dict[str, Any]], flight_record: dict[str, Any]) -> bool:
    """Check whether a matching flight already exists."""
    return any(
        record.get("Type") == "flight" and same_flight(record, flight_record)
        for record in records
    )
