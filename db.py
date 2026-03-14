import mysql.connector

# ─────────────────────────────────────────────
#  UPDATE THESE with your MySQL credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"   # <-- change this
DB_NAME = "hospital_db"
# ─────────────────────────────────────────────


def connect():
    """Return a new MySQL connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ── Patients ───────────────────────────────────

def create_patient(name, age, gender, phone, address):
    """Insert a new patient and return the generated ID."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age, gender, phone, address) VALUES (%s, %s, %s, %s, %s)",
        (name, age, gender, phone, address)
    )
    conn.commit()
    patient_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return patient_id


def get_patient(patient_id):
    """Fetch a single patient by ID. Returns a dict or None."""
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def search_patients(query):
    """Search patients by name or ID. Returns a list of dicts."""
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM patients WHERE name LIKE %s OR id = %s",
        (f"%{query}%", query if str(query).isdigit() else -1)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_all_patients():
    """Fetch all patients."""
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, age, gender FROM patients ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ── Lab Reports ────────────────────────────────

def save_lab_report(patient_id, tests):
    """
    Save lab test results for a patient.
    tests: list of (test_name, value, unit, normal_range)
    """
    conn = connect()
    cursor = conn.cursor()
    for test_name, value, unit, normal_range in tests:
        cursor.execute(
            "INSERT INTO lab_reports (patient_id, test_name, value, unit, normal_range) "
            "VALUES (%s, %s, %s, %s, %s)",
            (patient_id, test_name, value, unit, normal_range)
        )
    conn.commit()
    cursor.close()
    conn.close()


def get_reports(patient_id):
    """Fetch all lab reports for a patient. Returns list of dicts grouped by date."""
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM lab_reports WHERE patient_id = %s ORDER BY report_date DESC",
        (patient_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
