import tkinter as tk
from tkinter import messagebox

from record.client_crud import (
    create_client,
    delete_client,
    get_client_by_id,
    search_clients_by_name,
    update_client,
)


class ClientFormMixin:
    def get_client_fields(self, action: str) -> list[str]:
        if action == "create":
            return [
                "ID",
                "Name",
                "Address Line 1",
                "Address Line 2",
                "Address Line 3",
                "City",
                "State",
                "Zip Code",
                "Country",
                "Phone Number",
            ]
        if action in {"search", "delete"}:
            return ["ID or Name"]
        if action == "update":
            return [
                "ID",
                "Name",
                "Address Line 1",
                "Address Line 2",
                "Address Line 3",
                "City",
                "State",
                "Zip Code",
                "Country",
                "Phone Number",
            ]
        return []

    def handle_client_action(self, action: str) -> None:
        try:
            if action == "create":
                data = {
                    "ID": int(self.entries["ID"].get()),
                    "Name": self.entries["Name"].get(),
                    "Address Line 1": self.entries["Address Line 1"].get(),
                    "Address Line 2": self.entries["Address Line 2"].get(),
                    "Address Line 3": self.entries["Address Line 3"].get(),
                    "City": self.entries["City"].get(),
                    "State": self.entries["State"].get(),
                    "Zip Code": self.entries["Zip Code"].get(),
                    "Country": self.entries["Country"].get(),
                    "Phone Number": self.entries["Phone Number"].get(),
                }
                result = create_client(self.records, data)
                self.display_result(result)

            elif action == "search":
                value = self.entries["ID or Name"].get().strip()
                if value.isdigit():
                    result = get_client_by_id(self.records, int(value))
                else:
                    result = search_clients_by_name(self.records, value)
                self.display_result(result)

            elif action == "update":
                client_id = int(self.entries["ID"].get())
                updates = {
                    "Name": self.entries["Name"].get(),
                    "Address Line 1": self.entries["Address Line 1"].get(),
                    "Address Line 2": self.entries["Address Line 2"].get(),
                    "Address Line 3": self.entries["Address Line 3"].get(),
                    "City": self.entries["City"].get(),
                    "State": self.entries["State"].get(),
                    "Zip Code": self.entries["Zip Code"].get(),
                    "Country": self.entries["Country"].get(),
                    "Phone Number": self.entries["Phone Number"].get(),
                }
                result = update_client(self.records, client_id, updates)
                self.display_result(result)

            elif action == "delete":
                value = self.entries["ID or Name"].get().strip()
                if not value.isdigit():
                    raise ValueError("Delete for client requires numeric ID.")
                result = delete_client(self.records, int(value))
                self.display_result({"deleted": result})

        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
        except Exception as exc:
            messagebox.showerror("Unexpected Error", str(exc))
