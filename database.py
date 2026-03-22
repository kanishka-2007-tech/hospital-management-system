import sqlite3
from datetime import datetime
import hashlib

class Database:
    def __init__(self, db_name="hospital.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()
        self._seed_admin()

    def create_tables(self):
        c = self.conn.cursor()
        c.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role     TEXT DEFAULT 'staff'
            );
            CREATE TABLE IF NOT EXISTS patients (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL,
                age        TEXT,
                gender     TEXT,
                phone      TEXT,
                address    TEXT,
                disease    TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor     TEXT NOT NULL,
                department TEXT,
                date       TEXT NOT NULL,
                time       TEXT,
                notes      TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            );
        ''')
        self.conn.commit()

    def _seed_admin(self):
        if not self.get_user('admin'):
            pw = hashlib.sha256('admin123'.encode()).hexdigest()
            self.add_user('admin', pw, 'admin')

    # ── USERS ─────────────────────────────────────────────
    def add_user(self, username, password_hash, role='staff'):
        self.conn.execute(
            "INSERT INTO users (username,password,role) VALUES (?,?,?)",
            (username, password_hash, role))
        self.conn.commit()

    def get_user(self, username):
        return self.conn.execute(
            "SELECT id,username,password,role FROM users WHERE username=?",
            (username,)).fetchone()

    # ── PATIENTS ──────────────────────────────────────────
    def add_patient(self, name, age, gender, phone, address, disease):
        self.conn.execute(
            "INSERT INTO patients (name,age,gender,phone,address,disease) VALUES (?,?,?,?,?,?)",
            (name, age, gender, phone, address, disease))
        self.conn.commit()

    def get_all_patients(self):
        return self.conn.execute(
            "SELECT id,name,age,gender,phone,address,disease,created_at FROM patients ORDER BY id DESC"
        ).fetchall()

    def search_patients(self, q):
        like = f"%{q}%"
        return self.conn.execute(
            "SELECT id,name,age,gender,phone,address,disease,created_at FROM patients "
            "WHERE name LIKE ? OR disease LIKE ? OR phone LIKE ? ORDER BY id DESC",
            (like, like, like)).fetchall()

    def delete_patient(self, pid):
        self.conn.execute("DELETE FROM patients WHERE id=?", (pid,))
        self.conn.execute("DELETE FROM appointments WHERE patient_id=?", (pid,))
        self.conn.commit()

    # ── APPOINTMENTS ──────────────────────────────────────
    def add_appointment(self, patient_id, doctor, dept, date, time, notes):
        self.conn.execute(
            "INSERT INTO appointments (patient_id,doctor,department,date,time,notes) VALUES (?,?,?,?,?,?)",
            (patient_id, doctor, dept, date, time, notes))
        self.conn.commit()

    def get_all_appointments(self):
        return self.conn.execute('''
            SELECT a.id, a.patient_id, p.name, a.doctor, a.department,
                   a.date, a.time, a.notes
            FROM appointments a JOIN patients p ON a.patient_id=p.id
            ORDER BY a.date DESC, a.time DESC
        ''').fetchall()

    def delete_appointment(self, aid):
        self.conn.execute("DELETE FROM appointments WHERE id=?", (aid,))
        self.conn.commit()

    # ── STATS & CHARTS ────────────────────────────────────
    def get_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")
        total_p  = self.conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
        total_a  = self.conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
        today_a  = self.conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE date=?", (today,)).fetchone()[0]
        total_u  = self.conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        return dict(total_patients=total_p, total_appointments=total_a,
                    today_appointments=today_a, total_users=total_u)

    def patients_per_day(self):
        rows = self.conn.execute(
            "SELECT DATE(created_at) as d, COUNT(*) FROM patients "
            "GROUP BY d ORDER BY d DESC LIMIT 7").fetchall()
        return [{"date": r[0], "count": r[1]} for r in reversed(rows)]

    def appointments_per_dept(self):
        rows = self.conn.execute(
            "SELECT department, COUNT(*) FROM appointments "
            "GROUP BY department ORDER BY COUNT(*) DESC").fetchall()
        return [{"dept": r[0] or "General", "count": r[1]} for r in rows]
