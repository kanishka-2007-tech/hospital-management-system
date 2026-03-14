import tkinter as tk
from tkinter import messagebox
import patient
import lab_report
import search
import db


# ── Colours & fonts ──────────────────────────────────────────────────────────
COLOR_SIDEBAR   = "#1a237e"
COLOR_SIDEBAR_H = "#283593"
COLOR_BG        = "#f0f4f8"
COLOR_ACTIVE    = "#42a5f5"
FONT_TITLE      = ("Segoe UI", 13, "bold")
FONT_NAV        = ("Segoe UI", 12)


class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏥 Hospital Management System")
        self.geometry("1000x680")
        self.minsize(800, 550)
        self.configure(bg=COLOR_BG)
        self.resizable(True, True)

        # ── Check DB connection ──────────────────────────────────────
        try:
            db.connect()
        except Exception as e:
            messagebox.showerror(
                "Database Connection Failed",
                f"Could not connect to MySQL:\n\n{e}\n\n"
                "Please update DB_HOST, DB_USER, DB_PASSWORD in db.py and retry."
            )

        self._build_ui()
        self._show_register()   # default screen

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Left sidebar
        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="🏥 HMS",
                 font=("Segoe UI", 18, "bold"),
                 bg=COLOR_SIDEBAR, fg="white"
                 ).pack(pady=(30, 5))
        tk.Label(self.sidebar, text="Hospital Management",
                 font=("Segoe UI", 9), bg=COLOR_SIDEBAR, fg="#90caf9"
                 ).pack(pady=(0, 30))

        # Nav buttons
        self._nav_btns = {}
        nav_items = [
            ("📋  Register Patient", "register"),
            ("🔬  Lab Report",       "lab"),
            ("🔍  Search Patients",  "search"),
        ]
        for label, key in nav_items:
            btn = tk.Button(
                self.sidebar, text=label, font=FONT_NAV,
                bg=COLOR_SIDEBAR, fg="white", activebackground=COLOR_SIDEBAR_H,
                activeforeground="white", bd=0, relief="flat",
                padx=15, pady=12, anchor="w", cursor="hand2",
                command=lambda k=key: self._navigate(k)
            )
            btn.pack(fill="x")
            self._nav_btns[key] = btn

        # Divider + info at bottom
        tk.Frame(self.sidebar, bg=COLOR_ACTIVE, height=2).pack(fill="x", pady=40)
        tk.Label(self.sidebar, text="v1.0  |  Kanishka Gupta",
                 font=("Segoe UI", 8), bg=COLOR_SIDEBAR, fg="#90caf9"
                 ).pack(side="bottom", pady=10)

        # Right content area
        self.content = tk.Frame(self, bg=COLOR_BG)
        self.content.pack(side="right", fill="both", expand=True)

    # ── Navigation ─────────────────────────────────────────────────────────────
    def _navigate(self, key):
        # Highlight active button
        for k, btn in self._nav_btns.items():
            btn.config(bg=COLOR_ACTIVE if k == key else COLOR_SIDEBAR)

        if key == "register":
            self._show_register()
        elif key == "lab":
            lab_report.open_lab_report(self.content)
        elif key == "search":
            search.open_search(self.content)

    def _show_register(self):
        self._nav_btns["register"].config(bg=COLOR_ACTIVE)
        patient.open_register(self.content)


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()
