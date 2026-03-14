# ✅ Hospital Management System — Completed

## Files Created

| File | Purpose |
|------|---------|
| [setup_db.sql](file:///c:/Users/Kanishka/Desktop/github/hospital-management-system/setup_db.sql) | SQL script to create the database & tables |
| [db.py](file:///c:/Users/Kanishka/Desktop/github/hospital-management-system/db.py) | MySQL connection + all query functions |
| [patient.py](file:///c:/Users/Kanishka/Desktop/github/hospital-management-system/patient.py) | Patient Registration screen |
| [lab_report.py](file:///c:/Users/Kanishka/Desktop/github/hospital-management-system/lab_report.py) | Lab Test entry + auto report generation |
| [search.py](file:///c:/Users/Kanishka/Desktop/github/hospital-management-system/search.py) | Search patients + view past reports |
| [main.py](file:///c:/Users/Kanishka/Desktop/github/hospital-management-system/main.py) | App entry point + sidebar navigation |

---

## ⚙️ Setup Steps (Do These Once)

### 1. Install the MySQL driver
```
pip install mysql-connector-python
```

### 2. Create the database
Open MySQL Workbench (or any MySQL client) and run:
```sql
-- Copy-paste the contents of setup_db.sql and execute it
```

### 3. Update your DB credentials
Open [db.py](file:///c:/Users/Kanishka/Desktop/github/hospital-management-system/db.py) and change these lines to match your MySQL setup:
```python
DB_HOST     = "localhost"
DB_USER     = "root"
DB_PASSWORD = "your_password"   # ← change this
DB_NAME     = "hospital_db"
```

### 4. Run the app
```
python main.py
```

---

## 🖥️ App Screens

### 📋 Register Patient
- Fill in: Name, Age, Gender, Phone, Address
- Click **Register Patient** → a Patient ID is shown (save it!)

### 🔬 Lab Report
- Enter the **Patient ID**, click **Find** to confirm the patient
- Fill in test values (Blood Sugar, Hemoglobin, BP, etc.)
- Click **⚡ Generate Report** → a formatted report preview opens
- Click **💾 Save as .txt** to save the report file

### 🔍 Search Patients
- Type a name or ID in the search bar
- Click any patient row to view their lab report history at the bottom
