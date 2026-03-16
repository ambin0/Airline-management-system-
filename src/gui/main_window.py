import tkinter as tk
from tkinter import ttk

from gui.airline_form import AirlineFormMixin
from gui.client_form import ClientFormMixin
from gui.flight_form import FlightFormMixin


class RecordManagementApp(ClientFormMixin, AirlineFormMixin, FlightFormMixin):
    def __init__(self, root: tk.Tk, records: list[dict]):
        self.root = root
        self.records = records

        self.root.title("Record Management System")
        self.root.geometry("1000x700")

        self.record_type_var = tk.StringVar(value="client")
        self.action_var = tk.StringVar(value="create")
        self.entries = {}

        self.build_layout()
        self.refresh_form_fields()

    def build_layout(self) -> None:
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
        record_type_combo.bind("<<ComboboxSelected>>", lambda event: self.refresh_form_fields())

        ttk.Label(top_frame, text="Action:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        action_combo = ttk.Combobox(
            top_frame,
            textvariable=self.action_var,
            values=["create", "search", "update", "delete"],
            state="readonly",
            width=20,
        )
        action_combo.grid(row=0, column=3, padx=5, pady=5)
        action_combo.bind("<<ComboboxSelected>>", lambda event: self.refresh_form_fields())

        self.form_frame = ttk.LabelFrame(self.root, text="Input Form", padding=10)
        self.form_frame.pack(fill="x", padx=10, pady=10)

        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Execute", command=self.handle_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Show All Flights", command=self.show_all_flights).pack(side="left", padx=5)

        self.output_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_text = tk.Text(self.output_frame, wrap="word", height=20)
        self.output_text.pack(fill="both", expand=True)

    def refresh_form_fields(self) -> None:
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        self.entries = {}

        fields = self.get_fields_for_view(
            self.record_type_var.get(),
            self.action_var.get(),
        )

        for row, field in enumerate(fields):
            ttk.Label(self.form_frame, text=f"{field}:").grid(
                row=row, column=0, padx=5, pady=5, sticky="w"
            )
            entry = ttk.Entry(self.form_frame, width=50)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            self.entries[field] = entry

        if self.record_type_var.get() == "flight":
            ttk.Label(
                self.form_frame,
                text="Date format: YYYY-MM-DD HH:MM",
            ).grid(row=len(fields), column=0, columnspan=2, padx=5, pady=5, sticky="w")

    def get_fields_for_view(self, record_type: str, action: str) -> list[str]:
        if record_type == "client":
            return self.get_client_fields(action)
        if record_type == "airline":
            return self.get_airline_fields(action)
        if record_type == "flight":
            return self.get_flight_fields(action)
        return []

    def clear_form(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def handle_action(self) -> None:
        record_type = self.record_type_var.get()
        action = self.action_var.get()

        if record_type == "client":
            self.handle_client_action(action)
        elif record_type == "airline":
            self.handle_airline_action(action)
        elif record_type == "flight":
            self.handle_flight_action(action)

    def display_result(self, result) -> None:
        self.output_text.delete("1.0", tk.END)

        if result is None:
            self.output_text.insert(tk.END, "No matching record found.")
            return

        if result == []:
            self.output_text.insert(tk.END, "No matching records found.")
            return

        if isinstance(result, list):
            for item in result:
                self.output_text.insert(tk.END, f"{item}\n\n")
            return

        self.output_text.insert(tk.END, f"{result}")
