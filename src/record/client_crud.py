"""
Member 2 - Client CRUD

This module handles all the create, search, update, and delete stuff for client records.

Notes for teammates:
- Just like the other CRUD files, this only works on the shared `records` list in memory.
- The GUI team can call these functions directly.
- The storage team will handle saving/loading the records from the file separately.
"""

from typing import Any

from .crud_helpers import (
    delete_record_at_index,
    ensure_required_fields,
    find_record_index_by_id,
    find_records_by_field_contains,
    record_exists_by_id,
    update_record_fields,
)

CLIENT_TYPE = "client"


def create_client(records: list[dict[str, Any]], client_data: dict[str, Any]) -> dict[str, Any]:
    """Creates a new client record and adds it to the list."""
    ensure_required_fields(client_data, ["ID", "Name"])

    client_id = int(client_data["ID"])
    if record_exists_by_id(records, CLIENT_TYPE, client_id):
        raise ValueError(f"Client with ID {client_id} already exists.")

    # Building the new client record dictionary
    client_record = {
        "ID": client_id,
        "Type": CLIENT_TYPE,
        "Name": client_data.get("Name", ""),
        "Address Line 1": client_data.get("Address Line 1", ""),
        "Address Line 2": client_data.get("Address Line 2", ""),
        "Address Line 3": client_data.get("Address Line 3", ""),
        "City": client_data.get("City", ""),
        "State": client_data.get("State", ""),
        "Zip Code": client_data.get("Zip Code", ""),
        "Country": client_data.get("Country", ""),
        "Phone Number": client_data.get("Phone Number", ""),
    }

    records.append(client_record)
    return client_record


def get_client_by_id(records: list[dict[str, Any]], client_id: int) -> dict[str, Any] | None:
    """A simple helper to grab a client by their ID."""
    index = find_record_index_by_id(records, CLIENT_TYPE, client_id)
    if index == -1:
        return None
    return records[index]


def search_clients_by_name(records: list[dict[str, Any]], name: str) -> list[dict[str, Any]]:
    """Finds clients where their name contains the search text (case-insensitive)."""
    return find_records_by_field_contains(records, CLIENT_TYPE, "Name", name)


def update_client(
    records: list[dict[str, Any]],
    client_id: int,
    updates: dict[str, Any],
) -> dict[str, Any] | None:
    """Updates a client's record. Returns None if the client isn't found."""
    index = find_record_index_by_id(records, CLIENT_TYPE, client_id)
    if index == -1:
        return None

    # Make sure we don't change the ID or Type fields by accident
    return update_record_fields(records[index], updates, blocked_fields=["ID", "Type"])


def delete_client(records: list[dict[str, Any]], client_id: int) -> bool:
    """Deletes a client by their ID. Returns True if it worked, False otherwise."""
    index = find_record_index_by_id(records, CLIENT_TYPE, client_id)
    return delete_record_at_index(records, index)
