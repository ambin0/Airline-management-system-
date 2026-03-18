from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from tkinter import messagebox

from record.flight_crud import (
    create_flight,
    delete_flight,
    get_all_flights,
    search_flights,
    update_flight,
)


class FlightFormMixin:
    def get_flight_fields(self, action: str) -> list[str]:
        if action == "create":
            return ["Client_ID", "Airline_ID", "Date", "Start City", "End City"]
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
        if action == "delete":
            return ["Client_ID", "Airline_ID", "Date", "Start City", "End City"]
        return []

    def handle_flight_action(self, action: str) -> None:
        try:
            if action == "create":
                data = {
                    "Client_ID": int(self.entries["Client_ID"].get()),
                    "Airline_ID": int(self.entries["Airline_ID"].get()),
                    "Date": self.entries["Date"].get(),
                    "Start City": self.entries["Start City"].get(),
                    "End City": self.entries["End City"].get(),
                }
                result = create_flight(self.records, data)
                self.validate_flight_data(data)
                self.display_result(result)

            elif action == "search":
                criteria = self.build_flight_search_criteria()
                result = search_flights(self.records, criteria)
                self.display_result(result)

            elif action == "update":
                match_criteria = {
                    "Client_ID": int(self.entries["Client_ID"].get()),
                    "Airline_ID": int(self.entries["Airline_ID"].get()),
                    "Date": self.entries["Date"].get(),
                    "Start City": self.entries["Start City"].get(),
                    "End City": self.entries["End City"].get(),
                }
                self.validate_flight_data(match_criteria)
                updates = {
                    "Date": self.entries["New Date"].get() or self.entries["Date"].get(),
                    "Start City": self.entries["New Start City"].get() or self.entries["Start City"].get(),
                    "End City": self.entries["New End City"].get() or self.entries["End City"].get(),
                }
                result = update_flight(self.records, match_criteria, updates)
                self.display_result(result)

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
                
            elif action == "delete":
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

            except ValueError as exc:
                messagebox.showerror("Input Error", str(exc))
                self.status_var.set(f"Error: {exc}")
            except Exception as exc:
                messagebox.showerror("Unexpected Error", str(exc))
                self.status_var.set(f"Unexpected error: {exc}")

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

    def validate_flight_data(self, data: dict) -> None:
        if not str(data["Client_ID"]).isdigit():
            raise ValueError("Client ID must be a number.")
        if not str(data["Airline_ID"]).isdigit():
            raise ValueError("Airline ID must be a number.")
        if not data["Start City"].strip():
            raise ValueError("Start City is required.")
        if not data["End City"].strip():
            raise ValueError("End City is required.")
        try:
            datetime.strptime(data["Date"], "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Date must be in format YYYY-MM-DD HH:MM.")
