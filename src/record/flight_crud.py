"""
Member 2 - Flight CRUD

This one was a bit trickier. It handles all the CRUD for flight records.

Notes for teammates:
- The project brief doesn't give flights a standalone ID, which is a bit weird.
- So, for this module, we have to match flights using a combination of fields:
  Client_ID, Airline_ID, Date, Start City, and End City.
"""

from typing import Any

from .crud_helpers import (
    delete_record_at_index,
    ensure_required_fields,
    find_records_by_criteria,
    matches_criteria,
    update_record_fields,
)

FLIGHT_TYPE = "flight"


def build_flight_key(flight_data: dict[str, Any]) -> dict[str, Any]:
    """Helper to build the composite key we use to ID a flight."""
    return {
        "Client_ID": flight_data.get("Client_ID"),
        "Airline_ID": flight_data.get("Airline_ID"),
        "Date": flight_data.get("Date"),
        "Start City": flight_data.get("Start City"),
        "End City": flight_data.get("End City"),
    }


def create_flight(records: list[dict[str, Any]], flight_data: dict[str, Any]) -> dict[str, Any]:
    """Creates a new flight record."""
    ensure_required_fields(
        flight_data,
        ["Client_ID", "Airline_ID", "Date", "Start City", "End City"],
    )

    flight_record = {
        "Type": FLIGHT_TYPE,
        "Client_ID": int(flight_data["Client_ID"]),
        "Airline_ID": int(flight_data["Airline_ID"]),
        "Date": flight_data.get("Date", ""),
        "Start City": flight_data.get("Start City", ""),
        "End City": flight_data.get("End City", ""),
    }

    # Make sure we don't add the *exact* same flight twice.
    existing = find_records_by_criteria(records, FLIGHT_TYPE, build_flight_key(flight_record))
    if existing:
        raise ValueError("An identical flight record already exists.")

    records.append(flight_record)
    return flight_record


def get_all_flights(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Just returns all the flight records we have."""
    return [record for record in records if record.get("Type") == FLIGHT_TYPE]


def search_flights(
    records: list[dict[str, Any]],
    criteria: dict[str, Any],
) -> list[dict[str, Any]]:
    """Finds flights that match whatever criteria you give it."""
    return find_records_by_criteria(records, FLIGHT_TYPE, criteria)


def _find_unique_flight_index(
    records: list[dict[str, Any]],
    match_criteria: dict[str, Any],
) -> int:
    """
    Finds the index of a flight, but ONLY if there's exactly one match.
    This is super important for updating/deleting.

    Returns -1 if we find nothing.
    But it will raise a ValueError if it finds more than one, to be safe.
    """
    matched_indexes = [
        index
        for index, record in enumerate(records)
        if record.get("Type") == FLIGHT_TYPE and matches_criteria(record, match_criteria)
    ]

    if not matched_indexes:
        return -1

    if len(matched_indexes) > 1:
        # Safety first!
        raise ValueError("More than one flight matches the criteria. Please use more specific details.")

    return matched_indexes[0]


def update_flight(
    records: list[dict[str, Any]],
    match_criteria: dict[str, Any],
    updates: dict[str, Any],
) -> dict[str, Any] | None:
    """Updates a single flight, as long as the match criteria is unique."""
    index = _find_unique_flight_index(records, match_criteria)
    if index == -1:
        return None

    # Don't let anyone change the record Type!
    return update_record_fields(records[index], updates, blocked_fields=["Type"])


def delete_flight(
    records: list[dict[str, Any]],
    match_criteria: dict[str, Any],
) -> bool:
    """Deletes a single flight, as long as the match criteria is unique."""
    index = _find_unique_flight_index(records, match_criteria)
    return delete_record_at_index(records, index)
