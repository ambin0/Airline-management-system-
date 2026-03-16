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
        if action in {"update", "delete"}:
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
                updates = {
                    "Date": self.entries["New Date"].get() or self.entries["Date"].get(),
                    "Start City": self.entries["New Start City"].get() or self.entries["Start City"].get(),
                    "End City": self.entries["New End City"].get() or self.entries["End City"].get(),
                }
                result = update_flight(self.records, match_criteria, updates)
                self.display_result(result)

            elif action == "delete":
                match_criteria = {
                    "Client_ID": int(self.entries["Client_ID"].get()),
                    "Airline_ID": int(self.entries["Airline_ID"].get()),
                    "Date": self.entries["Date"].get(),
                    "Start City": self.entries["Start City"].get(),
                    "End City": self.entries["End City"].get(),
                }
                result = delete_flight(self.records, match_criteria)
                self.display_result({"deleted": result})

        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
        except Exception as exc:
            messagebox.showerror("Unexpected Error", str(exc))

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
