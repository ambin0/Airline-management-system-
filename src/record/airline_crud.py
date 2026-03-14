"""
Member 2 - Airline CRUD

Handles all the logic for creating, searching, updating, and deleting
the airline records. Pretty straightforward stuff.
"""

from typing import Any

# Grabbing our helper functions from the other file
from .crud_helpers import (
    delete_record_at_index,
    ensure_required_fields,
    find_record_index_by_id,
    find_records_by_field_contains,
    record_exists_by_id,
    update_record_fields,
)

AIRLINE_TYPE = "airline"


def create_airline(
    records: list[dict[str, Any]],
    airline_data: dict[str, Any],
) -> dict[str, Any]:
    """Creates a new airline record and adds it to our main list."""
    ensure_required_fields(airline_data, ["ID", "Company Name"])

    airline_id = int(airline_data["ID"])
    if record_exists_by_id(records, AIRLINE_TYPE, airline_id):
        # Can't have two airlines with the same ID, obviously.
        raise ValueError(f"Airline with ID {airline_id} already exists.")

    airline_record = {
        "ID": airline_id,
        "Type": AIRLINE_TYPE,
        "Company Name": airline_data.get("Company Name", ""),
    }

    records.append(airline_record)
    return airline_record


def get_airline_by_id(records: list[dict[str, Any]], airline_id: int) -> dict[str, Any] | None:
    """Just a simple helper to find an airline by its ID."""
    index = find_record_index_by_id(records, AIRLINE_TYPE, airline_id)
    if index != -1:
        return records[index]
    return None


def search_airlines_by_name(
    records: list[dict[str, Any]],
    company_name: str,
) -> list[dict[str, Any]]:
    """Returns a list of airlines where the company name contains the search text."""
    return find_records_by_field_contains(records, AIRLINE_TYPE, "Company Name", company_name)


def update_airline(
    records: list[dict[str, Any]],
    airline_id: int,
    updates: dict[str, Any],
) -> dict[str, Any] | None:
    """Updates an airline's info. Returns None if it doesn't exist."""
    index = find_record_index_by_id(records, AIRLINE_TYPE, airline_id)
    if index == -1:
        return None # Not found

    # Make sure we don't accidentally change the ID or Type
    return update_record_fields(records[index], updates, blocked_fields=["ID", "Type"])


def delete_airline(records: list[dict[str, Any]], airline_id: int) -> bool:
    """Deletes an airline from the list. Returns True if it worked."""
    index = find_record_index_by_id(records, AIRLINE_TYPE, airline_id)
    return delete_record_at_index(records, index)
