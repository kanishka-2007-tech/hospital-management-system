# 🏥 MediCore — Hospital Management Web App

A full-stack Flask web app with login, patient management, appointment booking, live charts, and REST API.

## 📝 About the App

MediCore is designed as a lightweight, easy-to-deploy hospital management system for small clinics and practice teams. It provides:

- Secure user authentication with admin, doctor, and staff roles.
- Patient record management with add/view/search/update/delete operations.
- Appointment scheduling, viewing, and cancellation workflow.
- Interactive analytics dashboards (charts and key performance indicators).
- REST API endpoints for integration with external tools or frontend clients.
- SQLite persistence for zero-dependency database management (in development mode).

This repo is ideal for learning Flask, implementing CRUD and authentication patterns, and showing a polished clinic dashboard demo.

---

## 📁 Project Structure

```
hospital_web/
├── app.py               ← Flask routes & REST API
├── database.py          ← SQLite database layer
├── requirements.txt     ← Dependencies
├── hospital.db          ← Auto-created on first run
└── templates/
    ├── base.html        ← Sidebar layout
    ├── login.html       ← Login page
    ├── register.html    ← Register page
    ├── dashboard.html   ← Stats + charts
    ├── patients.html    ← Patient list & search
    ├── add_patient.html ← Add patient form
    └── appointments.html← Book & view appointments
```

---

## 🚀 Setup & Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.7+** — [Download here](https://www.python.org/downloads/)
- **pip** — Comes with Python (check: `pip --version`)
- **Git** (optional) — For cloning the repo
- **A modern web browser** — Chrome, Firefox, Safari, or Edge

---

### Step-by-Step Installation

#### 1. **Clone or Download the Repository**

```bash
# Using Git
git clone https://github.com/your-username/hospital-management-system.git
cd hospital-management-system

# Or download as ZIP and extract manually
```

#### 2. **Create a Virtual Environment**

A virtual environment isolates project dependencies from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal prompt should now show `(venv)` at the beginning.

#### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

This installs all required packages listed in `requirements.txt` (Flask, Flask-SQLAlchemy, etc.).

**Verify installation:**
```bash
pip list
```

#### 4. **Initialize the Database**

The app uses SQLite and auto-creates the database on first run. To pre-initialize (optional):

```bash
python setup_db.sql
# Or let the app create it automatically when you start it
```

#### 5. **Run the Application**

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

#### 6. **Access the App**

Open your web browser and navigate to:

```
http://localhost:5000
```

#### 7. **Login with Default Credentials**

- **Username:** `admin`
- **Password:** `admin123`

You're now in the dashboard! Explore patient management, appointments, and analytics.

---

### Environment Variables (Optional)

If needed, create a `.env` file in the project root for configuration:

```
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=sqlite:///hospital.db
SECRET_KEY=your-secret-key-here
```

Then load it:
```bash
pip install python-dotenv
```

---

### Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` again |
| `Port 5000 already in use` | Change port: `python app.py --port=5001` or kill the process using port 5000 |
| `Database locked` | Delete `hospital.db` and restart the app |
| `Permission denied` (macOS/Linux) | Run `chmod +x app.py` or use `python app.py` instead of `./app.py` |
| Blank screen after login | Clear browser cache (Ctrl+Shift+Delete) and refresh |

---

### Deactivate Virtual Environment

When finished, deactivate the virtual environment:

```bash
deactivate
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 Auth | Login, Register, Role-based (admin/doctor/staff) |
| 👤 Patients | Add, View, Search, Delete |
| 📅 Appointments | Book, View, Cancel with modal UI |
| 📊 Charts | Line chart (patients/day) + Doughnut (by dept) |
| 🔌 REST API | `/api/stats`, `/api/patients`, `/api/appointments` |

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/stats` | Dashboard stats |
| GET | `/api/patients` | All patients (JSON) |
| GET | `/api/appointments` | All appointments (JSON) |
| GET | `/api/chart/patients-per-day` | Chart data |
| GET | `/api/chart/appointments-per-dept` | Chart data |
