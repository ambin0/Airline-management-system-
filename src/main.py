from __future__ import annotations

import tkinter as tk

from data.storage import close_application, load_records
from gui.main_window import RecordManagementApp


def main() -> None:
    records = load_records()

    root = tk.Tk()
    RecordManagementApp(root, records)
    root.protocol("WM_DELETE_WINDOW", lambda: close_application(records, root))
    root.mainloop()


if __name__ == "__main__":
    main()
