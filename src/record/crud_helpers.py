"""
Member 2 - CRUD helpers

Just a bunch of shared helper functions that the other CRUD modules use.
I put them here to avoid repeating myself all over the place.

Notes for teammates:
- These helpers only work on the in-memory `records` list.
- The storage part of the project should handle the file I/O stuff separately.
"""

from typing import Any


def ensure_required_fields(data: dict[str, Any], required_fields: list[str]) -> None:
    """Checks if all the required fields are actually in the data. Raises an error if not."""
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


def get_records_by_type(records: list[dict[str, Any]], record_type: str) -> list[dict[str, Any]]:
    """Filters the main list to get only records of a certain type (e.g., 'client')."""
    return [r for r in records if r.get("Type") == record_type]


def find_record_index_by_id(
    records: list[dict[str, Any]], record_type: str, record_id: int
) -> int:
    """Finds the list index for a record from its type and ID. Returns -1 if it's not there."""
    for i, record in enumerate(records):
        if record.get("Type") == record_type and record.get("ID") == record_id:
            return i
    return -1


def record_exists_by_id(
    records: list[dict[str, Any]], record_type: str, record_id: int
) -> bool:
    """Just a quick check to see if a record with a given ID already exists."""
    return find_record_index_by_id(records, record_type, record_id) != -1


def update_record_fields(
    record: dict[str, Any],
    updates: dict[str, Any],
    blocked_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Updates a record's fields, but protects a few important ones from being changed."""
    # if blocked_fields is None, make it an empty list
    blocked_fields = blocked_fields or []

    for key, value in updates.items():
        if key in blocked_fields:
            continue # skip protected fields

        # This makes partial updates easier, we can just pass in a dict with the fields
        # we want to change and the rest will be ignored if they are None.
        if value is None:
            continue

        record[key] = value

    return record


def delete_record_at_index(records: list[dict[str, Any]], index: int) -> bool:
    """Deletes a record using its list index. Returns True if it worked."""
    if 0 <= index < len(records):
        del records[index]
        return True
    return False


def find_records_by_field_contains(
    records: list[dict[str, Any]],
    record_type: str,
    field_name: str,
    value: str,
) -> list[dict[str, Any]]:
    """Does a case-insensitive search on a specific field."""
    search_value = str(value).strip().lower()
    if not search_value:
        return [] # don't return everything if the search is empty

    results = []
    for record in get_records_by_type(records, record_type):
        field_val = str(record.get(field_name, "")).strip().lower()
        if search_value in field_val:
            results.append(record)
    return results


def matches_criteria(record: dict[str, Any], criteria: dict[str, Any]) -> bool:
    """Checks if a record matches a dictionary of criteria."""
    for key, expected in criteria.items():
        # if a criterion is None or empty, we just ignore it
        if expected in (None, ""):
            continue

        actual = record.get(key)

        # doing a case-insensitive match for strings
        if isinstance(expected, str):
            if str(actual).strip().lower() != expected.strip().lower():
                return False
        else:
            if actual != expected:
                return False

    return True


def find_records_by_criteria(
    records: list[dict[str, Any]],
    record_type: str,
    criteria: dict[str, Any],
) -> list[dict[str, Any]]:
    """Finds all records of a specific type that match the given criteria."""
    return [
        record
        for record in records
        if record.get("Type") == record_type and matches_criteria(record, criteria)
    ]
