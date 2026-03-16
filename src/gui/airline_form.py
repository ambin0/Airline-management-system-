import tkinter as tk
from tkinter import messagebox

from record.airline_crud import (
    create_airline,
    delete_airline,
    get_airline_by_id,
    search_airlines_by_name,
    update_airline,
)


class AirlineFormMixin:
    def get_airline_fields(self, action: str) -> list[str]:
        if action == "create":
            return ["ID", "Company Name"]
        if action in {"search", "delete"}:
            return ["ID or Company Name"]
        if action == "update":
            return ["ID", "Company Name"]
        return []

    def handle_airline_action(self, action: str) -> None:
        try:
            if action == "create":
                data = {
                    "ID": int(self.entries["ID"].get()),
                    "Company Name": self.entries["Company Name"].get(),
                }
                result = create_airline(self.records, data)
                self.display_result(result)

            elif action == "search":
                value = self.entries["ID or Company Name"].get().strip()
                if value.isdigit():
                    result = get_airline_by_id(self.records, int(value))
                else:
                    result = search_airlines_by_name(self.records, value)
                self.display_result(result)

            elif action == "update":
                airline_id = int(self.entries["ID"].get())
                updates = {
                    "Company Name": self.entries["Company Name"].get()
                }
                result = update_airline(self.records, airline_id, updates)
                self.display_result(result)

            elif action == "delete":
                value = self.entries["ID or Company Name"].get().strip()
                if not value.isdigit():
                    raise ValueError("Delete for airline requires numeric ID.")
                result = delete_airline(self.records, int(value))
                self.display_result({"deleted": result})

        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
        except Exception as exc:
            messagebox.showerror("Unexpected Error", str(exc))
