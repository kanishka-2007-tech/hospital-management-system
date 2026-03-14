import tkinter as tk
from tkinter import ttk, messagebox
import db


FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 11)
COLOR_BG   = "#f0f4f8"
COLOR_BTN  = "#2196F3"
COLOR_BTN_FG = "white"


def open_register(parent_frame, on_success=None):
    """Render the Patient Registration form inside parent_frame."""
    # Clear frame
    for w in parent_frame.winfo_children():
        w.destroy()

    parent_frame.configure(bg=COLOR_BG)

    tk.Label(parent_frame, text="🏥  Register New Patient",
             font=("Segoe UI", 16, "bold"), bg=COLOR_BG, fg="#1a237e"
             ).grid(row=0, column=0, columnspan=2, pady=(20, 15))

    fields = [
        ("Full Name *",   "name"),
        ("Age *",         "age"),
        ("Phone",         "phone"),
        ("Address",       "address"),
    ]

    entries = {}
    for i, (label, key) in enumerate(fields, start=1):
        tk.Label(parent_frame, text=label, font=FONT_LABEL,
                 bg=COLOR_BG, anchor="w"
                 ).grid(row=i, column=0, sticky="w", padx=30, pady=6)
        e = tk.Entry(parent_frame, font=FONT_ENTRY, width=35, relief="solid")
        e.grid(row=i, column=1, padx=10, pady=6)
        entries[key] = e

    # Gender dropdown
    tk.Label(parent_frame, text="Gender *", font=FONT_LABEL,
             bg=COLOR_BG, anchor="w"
             ).grid(row=len(fields)+1, column=0, sticky="w", padx=30, pady=6)
    gender_var = tk.StringVar(value="Male")
    gender_cb = ttk.Combobox(parent_frame, textvariable=gender_var,
                              values=["Male", "Female", "Other"],
                              state="readonly", width=33, font=FONT_ENTRY)
    gender_cb.grid(row=len(fields)+1, column=1, padx=10, pady=6)

    # Result label
    result_var = tk.StringVar()
    tk.Label(parent_frame, textvariable=result_var, font=("Segoe UI", 11, "bold"),
             bg=COLOR_BG, fg="#2e7d32"
             ).grid(row=len(fields)+3, column=0, columnspan=2, pady=5)

    def submit():
        name    = entries["name"].get().strip()
        age_str = entries["age"].get().strip()
        phone   = entries["phone"].get().strip()
        address = entries["address"].get().strip()
        gender  = gender_var.get()

        if not name:
            messagebox.showerror("Validation", "Full Name is required.")
            return
        if not age_str.isdigit():
            messagebox.showerror("Validation", "Age must be a number.")
            return

        try:
            pid = db.create_patient(name, int(age_str), gender, phone, address)
            result_var.set(f"✅  Patient registered! Patient ID: {pid}")
            for e in entries.values():
                e.delete(0, tk.END)
            if on_success:
                on_success()
        except Exception as ex:
            messagebox.showerror("Database Error", str(ex))

    tk.Button(parent_frame, text="Register Patient", font=("Segoe UI", 11, "bold"),
              bg=COLOR_BTN, fg=COLOR_BTN_FG, relief="flat", padx=20, pady=8,
              cursor="hand2", command=submit
              ).grid(row=len(fields)+2, column=0, columnspan=2, pady=15)
