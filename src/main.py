from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from data.storage import close_application, load_records
from record.airline_crud import (
    create_airline,
    delete_airline,
    get_airline_by_id,
    search_airlines_by_name,
    update_airline,
)
from record.client_crud import (
    create_client,
    delete_client,
    get_client_by_id,
    search_clients_by_name,
    update_client,
)
from record.flight_crud import (
    create_flight,
    delete_flight,
    get_all_flights,
    search_flights,
    update_flight,
)


class RecordManagementApp:
    def __init__(self, root: tk.Tk, records: list[dict]):
        self.root = root
        self.records = records

        self.root.title("Record Management System")
        self.root.geometry("1000x700")

        self.record_type_var = tk.StringVar(value="client")
        self.action_var = tk.StringVar(value="create")

        self._build_layout()
        self._refresh_form_fields()

    def _build_layout(self) -> None:
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="Record Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        record_type_combo = ttk.Combobox(
            top_frame,
            textvariable=self.record_type_var,
            values=["client", "airline", "flight"],
            state="readonly",
            width=20,
        )
        record_type_combo.grid(row=0, column=1, padx=5, pady=5)
        record_type_combo.bind("<<ComboboxSelected>>", lambda event: self._refresh_form_fields())

        ttk.Label(top_frame, text="Action:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        action_combo = ttk.Combobox(
            top_frame,
            textvariable=self.action_var,
            values=["create", "search", "update", "delete"],
            state="readonly",
            width=20,
        )
        action_combo.grid(row=0, column=3, padx=5, pady=5)
        action_combo.bind("<<ComboboxSelected>>", lambda event: self._refresh_form_fields())

        self.form_frame = ttk.LabelFrame(self.root, text="Input Form", padding=10)
        self.form_frame.pack(fill="x", padx=10, pady=10)

        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Execute", command=self._handle_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self._clear_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Show All Flights", command=self._show_all_flights).pack(side="left", padx=5)

        self.output_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_text = tk.Text(self.output_frame, wrap="word", height=20)
        self.output_text.pack(fill="both", expand=True)

    def _refresh_form_fields(self) -> None:
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        self.entries: dict[str, tk.Entry] = {}

        record_type = self.record_type_var.get()
        action = self.action_var.get()
        fields = self._get_fields_for_view(record_type, action)

        for row, field in enumerate(fields):
            ttk.Label(self.form_frame, text=f"{field}:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.form_frame, width=50)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            self.entries[field] = entry

    def _get_fields_for_view(self, record_type: str, action: str) -> list[str]:
        if record_type == "client":
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

        if record_type == "airline":
            if action == "create":
                return ["ID", "Company Name"]
            if action in {"search", "delete"}:
                return ["ID or Company Name"]
            if action == "update":
                return ["ID", "Company Name"]

        if record_type == "flight":
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

    def _clear_form(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def _handle_action(self) -> None:
        record_type = self.record_type_var.get()
        action = self.action_var.get()

        try:
            if record_type == "client":
                self._handle_client_action(action)
            elif record_type == "airline":
                self._handle_airline_action(action)
            elif record_type == "flight":
                self._handle_flight_action(action)
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
        except Exception as exc:
            messagebox.showerror("Unexpected Error", str(exc))

    def _handle_client_action(self, action: str) -> None:
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
            self._display_result(result)

        elif action == "search":
            value = self.entries["ID or Name"].get().strip()
            if value.isdigit():
                result = get_client_by_id(self.records, int(value))
            else:
                result = search_clients_by_name(self.records, value)
            self._display_result(result)

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
            self._display_result(result)

        elif action == "delete":
            value = self.entries["ID or Name"].get().strip()
            if not value.isdigit():
                raise ValueError("Delete for client requires numeric ID.")
            result = delete_client(self.records, int(value))
            self._display_result({"deleted": result})

    def _handle_airline_action(self, action: str) -> None:
        if action == "create":
            data = {
                "ID": int(self.entries["ID"].get()),
                "Company Name": self.entries["Company Name"].get(),
            }
            result = create_airline(self.records, data)
            self._display_result(result)

        elif action == "search":
            value = self.entries["ID or Company Name"].get().strip()
            if value.isdigit():
                result = get_airline_by_id(self.records, int(value))
            else:
                result = search_airlines_by_name(self.records, value)
            self._display_result(result)

        elif action == "update":
            airline_id = int(self.entries["ID"].get())
            updates = {"Company Name": self.entries["Company Name"].get()}
            result = update_airline(self.records, airline_id, updates)
            self._display_result(result)

        elif action == "delete":
            value = self.entries["ID or Company Name"].get().strip()
            if not value.isdigit():
                raise ValueError("Delete for airline requires numeric ID.")
            result = delete_airline(self.records, int(value))
            self._display_result({"deleted": result})

    def _handle_flight_action(self, action: str) -> None:
        if action == "create":
            data = {
                "Client_ID": int(self.entries["Client_ID"].get()),
                "Airline_ID": int(self.entries["Airline_ID"].get()),
                "Date": self.entries["Date"].get(),
                "Start City": self.entries["Start City"].get(),
                "End City": self.entries["End City"].get(),
            }
            result = create_flight(self.records, data)
            self._display_result(result)

        elif action == "search":
            criteria = self._build_flight_search_criteria()
            result = search_flights(self.records, criteria)
            self._display_result(result)

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
            self._display_result(result)

        elif action == "delete":
            match_criteria = {
                "Client_ID": int(self.entries["Client_ID"].get()),
                "Airline_ID": int(self.entries["Airline_ID"].get()),
                "Date": self.entries["Date"].get(),
                "Start City": self.entries["Start City"].get(),
                "End City": self.entries["End City"].get(),
            }
            result = delete_flight(self.records, match_criteria)
            self._display_result({"deleted": result})

    def _build_flight_search_criteria(self) -> dict:
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

    def _show_all_flights(self) -> None:
        flights = get_all_flights(self.records)
        self._display_result(flights)

    def _display_result(self, result) -> None:
        self.output_text.delete("1.0", tk.END)

        if result is None:
            self.output_text.insert(tk.END, "No matching record found.")
            return

        if result == []:
            self.output_text.insert(tk.END, "No matching records found.")
            return

        if isinstance(result, list):
            for item in result:
                self.output_text.insert(tk.END, f"{item}

")
            return

        self.output_text.insert(tk.END, f"{result}")


def main() -> None:
    records = load_records()

    root = tk.Tk()
    RecordManagementApp(root, records)
    root.protocol("WM_DELETE_WINDOW", lambda: close_application(records, root))
    root.mainloop()


if __name__ == "__main__":
    main()
