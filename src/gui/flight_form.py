from datetime import datetime
from tkinter import messagebox
import tkinter as tk

# Import the flight CRUD functions from the backend
# they create, search, update, delete, and list all flight records

from record.flight_crud import (
    create_flight,
    delete_flight,
    get_all_flights,
    search_flights,
    update_flight,
)


class FlightFormMixin:
    # This tells the GUI which input fields to show
    # depending on the selected flight action
    def get_flight_fields(self, action: str) -> list[str]:
         # For create, the user must enter a full new flight record
        if action == "create":
            return ["Client_ID", "Airline_ID", "Date", "Start City", "End City"]
       # For search, the same fields are shown, but the user can fill in
        # only the ones they want to search by
        if action == "search":
            return ["Client_ID", "Airline_ID", "Date", "Start City", "End City"]
        if action == "update":
            return [
                "Client_ID",
                "Airline_ID",
                "Date",
                "Start City",
                "End City",
                "New Date",
                "New Start City",
                "New End City",
            ]
        if action == "delete": # For delete, the user only needs to enter the existing flight details
            return ["Client_ID", "Airline_ID", "Date", "Start City", "End City"]
        return []

    def handle_flight_action(self, action: str) -> None:
        try:
            if action == "create":   # CREATE FLIGHT
                data = {
                    "Client_ID": int(self.entries["Client_ID"].get()),
                    "Airline_ID": int(self.entries["Airline_ID"].get()),
                    "Date": self.entries["Date"].get(),
                    "Start City": self.entries["Start City"].get(),
                    "End City": self.entries["End City"].get(),
                }
                result = create_flight(self.records, data)
                self.validate_flight_data(data)  # Validate the input before sending it to the backend
                self.display_result(result)

            elif action == "search":    # SEARCH FLIGHT
                criteria = self.build_flight_search_criteria() # Build a search dictionary using only the fields the user filled in
                result = search_flights(self.records, criteria)
                self.display_result(result)

            elif action == "update":  # UPDATE FLIGHT
                match_criteria = {
                    "Client_ID": int(self.entries["Client_ID"].get()),
                    "Airline_ID": int(self.entries["Airline_ID"].get()),
                    "Date": self.entries["Date"].get(),
                    "Start City": self.entries["Start City"].get(),
                    "End City": self.entries["End City"].get(),
                }
                self.validate_flight_data(match_criteria)   # Validate the original flight details
                updates = {
                    "Date": self.entries["New Date"].get() or self.entries["Date"].get(),
                    "Start City": self.entries["New Start City"].get() or self.entries["Start City"].get(),
                    "End City": self.entries["New End City"].get() or self.entries["End City"].get(),
                }
                result = update_flight(self.records, match_criteria, updates)
                self.display_result(result)

                # Build the new updated version of the flight
                # If the user leaves a "New ..." field blank,
                # the old value is kept

                updated_record = {
                    "Client_ID": match_criteria["Client_ID"],
                    "Airline_ID": match_criteria["Airline_ID"],
                    "Date": self.entries["New Date"].get() or self.entries["Date"].get(),
                    "Start City": self.entries["New Start City"].get() or self.entries["Start City"].get(),
                    "End City": self.entries["New End City"].get() or self.entries["End City"].get(),
                    }
                self.validate_flight_data(updated_record)
                updates = {
                    "Date": updated_record["Date"],
                    "Start City": updated_record["Start City"],
                    "End City": updated_record["End City"],
                    }
                
            elif action == "delete": # DELETE FLIGHT
                match_criteria = {
                    "Client_ID": int(self.entries["Client_ID"].get()),
                    "Airline_ID": int(self.entries["Airline_ID"].get()),
                    "Date": self.entries["Date"].get(),
                    "Start City": self.entries["Start City"].get(),
                    "End City": self.entries["End City"].get(),
                }
                result = delete_flight(self.records, match_criteria)
                self.validate_flight_data(match_criteria)
                self.display_result({"deleted": result})

            except ValueError as exc:  # Handles expected input mistakes, such as bad IDs or wrong date format
                messagebox.showerror("Input Error", str(exc))
                self.status_var.set(f"Error: {exc}")
            except Exception as exc:
                messagebox.showerror("Unexpected Error", str(exc))
                self.status_var.set(f"Unexpected error: {exc}")

 # This builds a search dictionary from the flight search form
 # It only includes fields that the user actually filled in

    def build_flight_search_criteria(self) -> dict:
        criteria = {}
        for key in ["Client_ID", "Airline_ID", "Date", "Start City", "End City"]:
            raw_value = self.entries[key].get().strip()
            if not raw_value:
                continue
            if key in {"Client_ID", "Airline_ID"}:
                criteria[key] = int(raw_value)
            else:
                criteria[key] = raw_value
        return criteria

    def show_all_flights(self) -> None:
        flights = get_all_flights(self.records)
        self.display_result(flights)

# This method checks whether a flight record is valid
    def validate_flight_data(self, data: dict) -> None:
        if not str(data["Client_ID"]).isdigit(): # Client ID must be numeric
            raise ValueError("Client ID must be a number.")
        if not str(data["Airline_ID"]).isdigit():
            raise ValueError("Airline ID must be a number.")
        if not data["Start City"].strip():
            raise ValueError("Start City is required.")
        if not data["End City"].strip():
            raise ValueError("End City is required.")
        try:
            datetime.strptime(data["Date"], "%Y-%m-%d %H:%M")  # Date must match the required format exactly
        except ValueError:
            raise ValueError("Date must be in format YYYY-MM-DD HH:MM.")
