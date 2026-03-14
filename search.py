import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import db


FONT_LABEL = ("Segoe UI", 11)
COLOR_BG   = "#f0f4f8"
COLOR_BTN  = "#2196F3"


def open_search(parent_frame):
    """Render the Search screen inside parent_frame."""
    for w in parent_frame.winfo_children():
        w.destroy()

    parent_frame.configure(bg=COLOR_BG)

    tk.Label(parent_frame, text="🔍  Search Patients",
             font=("Segoe UI", 16, "bold"), bg=COLOR_BG, fg="#1a237e"
             ).grid(row=0, column=0, columnspan=3, pady=(20, 10))

    # ── Search bar ───────────────────────────────────────────────────
    tk.Label(parent_frame, text="Name or ID:", font=FONT_LABEL,
             bg=COLOR_BG).grid(row=1, column=0, sticky="w", padx=20)
    search_var = tk.StringVar()
    search_entry = tk.Entry(parent_frame, textvariable=search_var,
                            font=FONT_LABEL, width=30, relief="solid")
    search_entry.grid(row=1, column=1, padx=8, pady=8)

    def do_search():
        query = search_var.get().strip()
        if not query:
            load_all()
            return
        results = db.search_patients(query)
        _populate_table(results)

    tk.Button(parent_frame, text="Search", font=FONT_LABEL,
              bg=COLOR_BTN, fg="white", relief="flat", padx=12,
              command=do_search
              ).grid(row=1, column=2, padx=4)

    search_entry.bind("<Return>", lambda e: do_search())

    # ── Results table ─────────────────────────────────────────────────
    cols = ("ID", "Name", "Age", "Gender")
    style = ttk.Style()
    style.configure("Custom.Treeview.Heading", font=("Segoe UI", 10, "bold"),
                    background="#1a237e", foreground="white")
    style.configure("Custom.Treeview", font=("Segoe UI", 10), rowheight=28)

    tree = ttk.Treeview(parent_frame, columns=cols, show="headings",
                        style="Custom.Treeview", height=12)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120 if col != "Name" else 200, anchor="center")
    tree.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

    scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=2, column=3, sticky="ns", pady=10)

    # ── Report detail area ────────────────────────────────────────────
    detail_frame = tk.Frame(parent_frame, bg=COLOR_BG)
    detail_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

    report_text = tk.Text(detail_frame, font=("Courier New", 9), height=10,
                          bg="#0d1117", fg="#c9d1d9", relief="flat", padx=8, pady=8, wrap="none")
    report_text.pack(fill="both", expand=True)
    report_text.config(state="disabled")

    def _populate_table(results):
        tree.delete(*tree.get_children())
        for p in results:
            tree.insert("", "end", iid=p["id"],
                        values=(p["id"], p["name"], p["age"], p["gender"]))

    def load_all():
        patients = db.get_all_patients()
        _populate_table(patients)

    def on_select(event):
        selected = tree.focus()
        if not selected:
            return
        pid = int(selected)
        patient = db.get_patient(pid)
        reports = db.get_reports(pid)

        report_text.config(state="normal")
        report_text.delete("1.0", "end")

        if patient:
            header = (
                f"  Patient: {patient['name']}  |  ID: {patient['id']}  |  "
                f"Age: {patient['age']}  |  Gender: {patient['gender']}\n"
                + "─" * 70 + "\n"
            )
            report_text.insert("end", header)

        if reports:
            for r in reports:
                dt = r["report_date"]
                if isinstance(dt, datetime):
                    dt = dt.strftime("%d-%b-%Y %H:%M")
                line = (
                    f"  {r['test_name']:<30} {r['value']:<12} "
                    f"{r['unit']:<12} Normal: {r['normal_range']}   [{dt}]\n"
                )
                report_text.insert("end", line)
        else:
            report_text.insert("end", "  No lab reports found for this patient.\n")

        report_text.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", on_select)

    # Load all patients on open
    load_all()
