# 🏥 Hospital Management System

A desktop application built with **Python** and **MySQL** that stores patient information and automatically generates lab reports based on the entered details.

## 💡 Project Idea

The core idea of this application is to digitalize the patient management workflow in a hospital or clinic. Staff can enter a patient's personal and medical details into the system, and the application will automatically generate a formatted **lab report** based on those inputs — eliminating manual paperwork and reducing errors.

## ✨ Features

- 📋 **Patient Registration** — Store patient name, age, gender, contact info, and medical history
- 🔬 **Lab Test Entry** — Input lab test results (e.g., blood tests, urine tests, etc.)
- 📄 **Auto Report Generation** — Generate a structured lab report based on entered patient details and test results
- 🗄️ **Database Integration** — All data is stored persistently using MySQL
- 🔍 **Search & Retrieve** — Look up patient records and their past reports

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core application logic |
| MySQL | Database for storing patient & report data |

## � Installation

### Prerequisites
- **Python 3.7+** installed on your system
- **MySQL Server** running locally or remotely
- **MySQL Connector/Python** package

### Steps
1. **Clone or download** this repository to your local machine.

2. **Install Python dependencies:**
   ```bash
   pip install mysql-connector-python
   ```

3. **Set up the MySQL database:**
   - Open MySQL command line or a MySQL client (like phpMyAdmin)
   - Run the `setup_db.sql` script to create the database and tables:
     ```sql
     -- Copy and paste the contents of setup_db.sql
     ```

4. **Configure database connection:**
   - Open `db.py` and update the database credentials if needed:
     ```python
     DB_HOST = "localhost"  # or your MySQL host
     DB_USER = "root"       # your MySQL username
     DB_PASSWORD = "your_password"  # your MySQL password
     DB_NAME = "hospital_db"
     ```

## 🚀 Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Using the application:**
   - **Patient Registration:** Click on "Register Patient" to add new patient details
   - **Lab Test Entry:** Select a patient and enter lab test results
   - **Generate Reports:** The system automatically generates formatted lab reports
   - **Search:** Use the search functionality to find patient records and reports

3. **Navigation:**
   - Use the sidebar to switch between different sections
   - All patient data and reports are stored in the MySQL database

## �👤 Author

**Kanishka Gupta**  
Software Engineer

