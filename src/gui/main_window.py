import tkinter as tk
from tkinter import ttk

# Import the three mixin classes, each one handles a different part of the GUI
# Client, Airline and flight actions

from gui.airline_form import AirlineFormMixin
from gui.client_form import ClientFormMixin
from gui.flight_form import FlightFormMixin

# This is the main GUI class for the whole app
# from the three mixin classes so it can use
# all the client, airline, and flight methods

class RecordManagementApp(ClientFormMixin, AirlineFormMixin, FlightFormMixin):
    def __init__(self, root: tk.Tk, records: list[dict]):
        self.root = root
        self.records = records

        self.root.title("Simply A Tourism - Record Management System") # Set the app window title and size
        self.root.geometry("1000x700")
        
        # Default screen starts as "create client"
        self.record_type_var = tk.StringVar(value="client")
        self.action_var = tk.StringVar(value="create")
        self.entries = {} # Example: self.entries["Name"] = the Name input box

        self.build_layout()
        self.refresh_form_fields()

    def build_layout(self) -> None:
        # Main title shown at the top of the app
        title_label = ttk.Label(
        self.root,
        text="Simply A Tourism",
        font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(10, 0))
        # Subtitle 
        subtitle_label = ttk.Label(
            self.root,
            text="Record Management System", 
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=(0, 10))
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="Record Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Label and dropdown for record type
        record_type_combo = ttk.Combobox(
            top_frame,
            textvariable=self.record_type_var,
            values=["client", "airline", "flight"],
            state="readonly",
            width=20,
        )
        record_type_combo.grid(row=0, column=1, padx=5, pady=5)
        record_type_combo.bind("<<ComboboxSelected>>", lambda event: self.refresh_form_fields())   # When the user changes record type, rebuild the form fields

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

         # This frame holds the dynamic form fields
        # Its title changes depending on the selected task
        
        self.form_frame = ttk.LabelFrame(self.root, text="Input Form", padding=10)
        self.form_frame.pack(fill="x", padx=10, pady=10)

        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill="x")

        # Main action button
        # Its text changes dynamically, e.g. "Create Client", "Search Flight"
        
        self.action_button = ttk.Button(button_frame, text="Execute", command=self.handle_action)
        self.action_button.pack(side="left", padx=5)    
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_form).pack(side="left", padx=5)

        # Button to show every flight record
        # This is only enabled when the current record type is flight
        
        self.show_flights_button = ttk.Button(button_frame, text="Show All Flights", command=self.show_all_flights)
        self.show_flights_button.pack(side="left", padx=5)

        self.output_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=10)

       # Status variable stores short feedback like:
        # "Ready", "Action completed successfully", "No matching records found"
        self.status_var = tk.StringVar(value="Ready")
        
        status_label = ttk.Label(self.root, textvariable=self.status_var)
        status_label.pack(fill="x", padx=10, pady=(0, 10))

        self.output_text = tk.Text(self.output_frame, wrap="word", height=20)
        self.output_text.pack(fill="both", expand=True)

    def refresh_form_fields(self) -> None:
        for widget in self.form_frame.winfo_children():
            widget.destroy()  #rebuilt when the user changes action/type

        self.entries = {}

        fields = self.get_fields_for_view(
            self.record_type_var.get(),
            self.action_var.get(),
        )
         # Build a task name like "Create Client" or "Update Flight"
        task_name = f"{self.action_var.get().title()} {self.record_type_var.get().title()}"
        self.form_frame.config(text=f"{task_name} Form")
        self.action_button.config(text=task_name)
        
        for row, field in enumerate(fields):
            ttk.Label(self.form_frame, text=f"{field}:").grid(
                row=row, column=0, padx=5, pady=5, sticky="w"
            )
            entry = ttk.Entry(self.form_frame, width=50)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            self.entries[field] = entry

            if self.record_type_var.get() == "flight":
                label_text = field
            if field in required_fields.get(self.record_type_var.get(), set()):
                label_text = f"{field} *"
            
        # Fields that should show a * because they are required
        required_fields = {
        "client": {"ID", "Name", "Phone Number"},
        "airline": {"ID", "Airline Name"},
        "flight": {"Client_ID", "Airline_ID", "Date", "Start City", "End City"},
            }
        
        ttk.Label(self.form_frame, text=f"{label_text}:").grid(
            row=row, column=0, padx=5, pady=5, sticky="w"
)
 # Only enable the "Show All Flights" button when flight is selected
        if self.record_type_var.get() == "flight":
            self.show_flights_button.config(state="normal")
        else:
            self.show_flights_button.config(state="disabled")
    
# Send the action to the correct mixin handler
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
        record_type = self.record_type_var.get() # Find the currently selected record type and action
        action = self.action_var.get()

        if record_type == "client":
            self.handle_client_action(action)
        elif record_type == "airline":
            self.handle_airline_action(action)
        elif record_type == "flight":
            self.handle_flight_action(action)

    def display_result(self, result) -> None:
        self.output_text.delete("1.0", tk.END) #clear old tect first

        if result is None: #if nothing was found
            self.output_text.insert(tk.END, "No matching record found.")
            self.status_var.set("No matching record found.")
            return

        if result == []: #if an empty list was returned
            self.output_text.insert(tk.END, "No matching records found.")
            self.status_var.set("No matching records found.")
            return
      # If the result is a list, show each item clearly
        if isinstance(result, list):
            self.output_text.insert(tk.END, f"Found {len(result)} record(s).\n\n")
            for index, item in enumerate(result, start=1):
                self.output_text.insert(tk.END, f"Record {index}\n")
                self.output_text.insert(tk.END, "-" * 40 + "\n")
                if isinstance(item, dict):
                    for key, value in item.items():
                        self.output_text.insert(tk.END, f"{key}: {value}\n")
                else:
                    self.output_text.insert(tk.END, f"{item}\n")
                self.output_text.insert(tk.END, "\n")
            self.status_var.set(f"Found {len(result)} record(s).")
            return
  # If the result is a single dictionary, print each key-value pair
        if isinstance(result, dict):
            for key, value in result.items():
                self.output_text.insert(tk.END, f"{key}: {value}\n")
            self.status_var.set("Action completed successfully.")
            return

        self.output_text.insert(tk.END, str(result))
        self.status_var.set("Action completed.")
