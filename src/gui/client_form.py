import tkinter as tk
import re
from tkinter import messagebox

# Import the client CRUD functions from the backend
# To create, search, update, and delete 
from record.client_crud import (
    create_client,
    delete_client,
    get_client_by_id,
    search_clients_by_name,
    update_client,
)


class ClientFormMixin:
    # checks whether the client data entered by the user is valid
    # It raises an error if something important is missing or formatted badly
    def validate_client_data(self, data: dict) -> None:
        if not str(data["ID"]).isdigit():
            raise ValueError("Client ID must be a number.")
        if not data["Name"].strip():
            raise ValueError("Name is required.")
        if not data["Phone Number"].strip():
            raise ValueError("Phone Number is required.")
        if not re.fullmatch(r"[0-9+\-\s()]+", data["Phone Number"]): # stops invalid characters
            raise ValueError("Phone Number contains invalid characters.")
        if data["Zip Code"] and len(data["Zip Code"].strip()) < 3:
            raise ValueError("ZIP Code looks too short.")
            
    # This tells the GUI which input fields to show
    # depending on the action selected by the user    
    def get_client_fields(self, action: str) -> list[str]:
        if action == "create": #show all for create
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
        if action in {"search", "delete"}: #only shows ID or Name for search and delete
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
                self.validate_client_data(data) # validates before sending to back end
                result = create_client(self.records, data)
                self.display_result(result)
                
            elif action == "search":
                value = self.entries["ID or Name"].get().strip()
                if value.isdigit():             # If it is all digits, search by ID
                    result = get_client_by_id(self.records, int(value))
                else:
                    result = search_clients_by_name(self.records, value)
                self.display_result(result)

            elif action == "update":  # UPDATE CLIENT
                client_id = int(self.entries["ID"].get())
                updates = {
                    "ID": client_id,
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
                self.validate_client_data(updates)

                # Send the updated values to the backend
                # We do not send the ID as part of the changes dictionary,
                # because the ID is used to find which record to update
                
                result = update_client(
                    self.records,
                    client_id,
                    {
                        "Name": updates["Name"],
                        "Address Line 1": updates["Address Line 1"],
                        "Address Line 2": updates["Address Line 2"],
                        "Address Line 3": updates["Address Line 3"],
                        "City": updates["City"],
                        "State": updates["State"],
                        "Zip Code": updates["Zip Code"],
                        "Country": updates["Country"],
                        "Phone Number": updates["Phone Number"],
                    },
                )
                self.display_result(result)
                
            elif action == "delete":  # DELETE CLIENT
                value = self.entries["ID or Name"].get().strip()
                if not value.isdigit():     # Delete only works by numeric ID
                    raise ValueError("Delete for client requires numeric ID.")
                result = delete_client(self.records, int(value))
                self.display_result({"deleted": result})

        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
            self.status_var.set(f"Error: {exc}")    # Also update the status line in the GUI
            
        except Exception as exc:
            messagebox.showerror("Unexpected Error", str(exc))
            self.status_var.set(f"Unexpected error: {exc}")
