import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import db


FONT_LABEL   = ("Segoe UI", 10)
FONT_ENTRY   = ("Segoe UI", 10)
COLOR_BG     = "#f0f4f8"
COLOR_BTN    = "#2196F3"
COLOR_BTN_FG = "white"

# Default lab tests: (Test Name, Unit, Normal Range)
DEFAULT_TESTS = [
    ("Blood Sugar (Fasting)",  "mg/dL",  "70 - 110"),
    ("Hemoglobin",             "g/dL",   "12 - 17"),
    ("WBC Count",              "10³/µL", "4.5 - 11.0"),
    ("RBC Count",              "10⁶/µL", "4.5 - 5.5"),
    ("Platelet Count",         "10³/µL", "150 - 400"),
    ("Systolic BP",            "mmHg",   "90 - 120"),
    ("Diastolic BP",           "mmHg",   "60 - 80"),
    ("Creatinine",             "mg/dL",  "0.6 - 1.2"),
    ("Uric Acid",              "mg/dL",  "3.5 - 7.0"),
    ("Cholesterol (Total)",    "mg/dL",  "< 200"),
]


def open_lab_report(parent_frame):
    """Render the Lab Report entry screen inside parent_frame."""
    for w in parent_frame.winfo_children():
        w.destroy()

    parent_frame.configure(bg=COLOR_BG)

    tk.Label(parent_frame, text="🔬  Lab Report Entry",
             font=("Segoe UI", 16, "bold"), bg=COLOR_BG, fg="#1a237e"
             ).grid(row=0, column=0, columnspan=4, pady=(20, 5))

    # ── Patient selector ─────────────────────────────────────────────
    tk.Label(parent_frame, text="Patient ID:", font=FONT_LABEL,
             bg=COLOR_BG).grid(row=1, column=0, sticky="w", padx=20, pady=6)
    pid_entry = tk.Entry(parent_frame, font=FONT_ENTRY, width=10, relief="solid")
    pid_entry.grid(row=1, column=1, sticky="w", pady=6)

    patient_label = tk.Label(parent_frame, text="", font=("Segoe UI", 10, "italic"),
                             bg=COLOR_BG, fg="#555")
    patient_label.grid(row=1, column=2, columnspan=2, sticky="w", padx=10)

    def lookup_patient():
        pid = pid_entry.get().strip()
        if not pid.isdigit():
            patient_label.config(text="⚠ Enter a valid numeric Patient ID", fg="red")
            return
        p = db.get_patient(int(pid))
        if p:
            patient_label.config(
                text=f"✅  {p['name']}  |  Age: {p['age']}  |  {p['gender']}", fg="#2e7d32"
            )
        else:
            patient_label.config(text="❌  Patient not found", fg="red")

    tk.Button(parent_frame, text="Find", font=FONT_LABEL,
              bg=COLOR_BTN, fg=COLOR_BTN_FG, relief="flat", padx=8,
              command=lookup_patient
              ).grid(row=1, column=1, sticky="e", padx=(0, 5))

    # ── Header row ───────────────────────────────────────────────────
    headers = ["Test Name", "Value", "Unit", "Normal Range"]
    for col, h in enumerate(headers):
        tk.Label(parent_frame, text=h, font=("Segoe UI", 10, "bold"),
                 bg="#1a237e", fg="white", padx=8, pady=4, relief="flat"
                 ).grid(row=2, column=col, sticky="ew", padx=2, pady=(15, 2))

    # ── Test rows ────────────────────────────────────────────────────
    test_entries = []   # list of (name_label, value_entry, unit_label, range_label)
    for i, (tname, unit, nrange) in enumerate(DEFAULT_TESTS):
        row = i + 3
        bg = "#ffffff" if i % 2 == 0 else "#e8f0fe"

        tk.Label(parent_frame, text=tname, font=FONT_LABEL, bg=bg,
                 anchor="w", padx=6).grid(row=row, column=0, sticky="ew", padx=2, pady=1)

        val_e = tk.Entry(parent_frame, font=FONT_ENTRY, width=12, relief="solid")
        val_e.grid(row=row, column=1, padx=4, pady=1)

        tk.Label(parent_frame, text=unit, font=FONT_LABEL, bg=bg,
                 padx=6).grid(row=row, column=2, sticky="ew", padx=2, pady=1)
        tk.Label(parent_frame, text=nrange, font=FONT_LABEL, bg=bg,
                 padx=6).grid(row=row, column=3, sticky="ew", padx=2, pady=1)

        test_entries.append((tname, val_e, unit, nrange))

    # ── Buttons ───────────────────────────────────────────────────────
    btn_row = len(DEFAULT_TESTS) + 3

    def generate_report():
        pid = pid_entry.get().strip()
        if not pid.isdigit():
            messagebox.showerror("Error", "Enter a valid Patient ID first.")
            return
        patient = db.get_patient(int(pid))
        if not patient:
            messagebox.showerror("Error", "Patient not found. Please register first.")
            return

        tests_data = []
        for tname, val_e, unit, nrange in test_entries:
            val = val_e.get().strip()
            if val:
                tests_data.append((tname, val, unit, nrange))

        if not tests_data:
            messagebox.showwarning("No Data", "Please enter at least one test value.")
            return

        # Save to DB
        db.save_lab_report(int(pid), tests_data)

        # Build report text
        now = datetime.now().strftime("%d-%b-%Y  %H:%M")
        sep = "─" * 60
        lines = [
            "=" * 60,
            "         HOSPITAL MANAGEMENT SYSTEM",
            "              LABORATORY REPORT",
            "=" * 60,
            f"  Patient Name : {patient['name']}",
            f"  Patient ID   : {patient['id']}",
            f"  Age / Gender : {patient['age']} yrs / {patient['gender']}",
            f"  Date & Time  : {now}",
            sep,
            f"  {'TEST NAME':<30} {'VALUE':<12} {'UNIT':<12} NORMAL RANGE",
            sep,
        ]
        for tname, val, unit, nrange in tests_data:
            lines.append(f"  {tname:<30} {val:<12} {unit:<12} {nrange}")
        lines += [sep, "  * Report generated by Hospital Management System *", "=" * 60]

        report_text = "\n".join(lines)
        _show_report_window(parent_frame.winfo_toplevel(), report_text)

    tk.Button(parent_frame, text="⚡ Generate Report", font=("Segoe UI", 11, "bold"),
              bg="#43a047", fg="white", relief="flat", padx=20, pady=8,
              cursor="hand2", command=generate_report
              ).grid(row=btn_row, column=0, columnspan=4, pady=20)


def _show_report_window(root, report_text):
    """Open a popup window showing the formatted lab report."""
    win = tk.Toplevel(root)
    win.title("Lab Report Preview")
    win.configure(bg="#1a1a2e")
    win.geometry("680x600")
    win.resizable(True, True)

    tk.Label(win, text="📄  Lab Report", font=("Segoe UI", 14, "bold"),
             bg="#1a1a2e", fg="white").pack(pady=(15, 5))

    text_box = tk.Text(win, font=("Courier New", 10), bg="#0d1117", fg="#c9d1d9",
                       relief="flat", padx=10, pady=10, wrap="none")
    text_box.pack(fill="both", expand=True, padx=20)
    text_box.insert("1.0", report_text)
    text_box.config(state="disabled")

    # Scrollbar
    sb = tk.Scrollbar(win, command=text_box.yview)
    sb.pack(side="right", fill="y")
    text_box.config(yscrollcommand=sb.set)

    def save_report():
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Lab Report"
        )
        if path:
            with open(path, "w") as f:
                f.write(report_text)
            messagebox.showinfo("Saved", f"Report saved to:\n{path}")

    tk.Button(win, text="💾  Save as .txt", font=("Segoe UI", 10, "bold"),
              bg=COLOR_BTN, fg="white", relief="flat", padx=16, pady=6,
              command=save_report
              ).pack(pady=12)
