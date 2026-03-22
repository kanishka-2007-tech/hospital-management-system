from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from database import Database
from functools import wraps
from datetime import datetime
import hashlib, os

app = Flask(__name__)
app.secret_key = os.urandom(24)
db = Database()

# ── AUTH HELPER ───────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ── AUTH ROUTES ───────────────────────────────────────────
@app.route('/', methods=['GET','POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        user = db.get_user(username)
        if user and user[2] == hash_pw(password):
            session['user'] = username
            session['role'] = user[3]
            return redirect(url_for('dashboard'))
        error = "Invalid username or password."
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        role     = request.form.get('role','staff')
        if db.get_user(username):
            error = "Username already exists."
        else:
            db.add_user(username, hash_pw(password), role)
            flash("Account created! Please login.")
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── MAIN PAGES ────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    stats = db.get_stats()
    now = datetime.now().strftime("%A, %d %B %Y")
    return render_template('dashboard.html', stats=stats,
                           user=session['user'], role=session['role'], now=now)

@app.route('/patients')
@login_required
def patients():
    q = request.args.get('q','')
    data = db.search_patients(q) if q else db.get_all_patients()
    return render_template('patients.html', patients=data, query=q,
                           user=session['user'])

@app.route('/patients/add', methods=['GET','POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        db.add_patient(
            request.form['name'], request.form['age'],
            request.form['gender'], request.form['phone'],
            request.form['address'], request.form['disease']
        )
        flash("Patient added successfully!")
        return redirect(url_for('patients'))
    return render_template('add_patient.html', user=session['user'])

@app.route('/patients/delete/<int:pid>', methods=['POST'])
@login_required
def delete_patient(pid):
    db.delete_patient(pid)
    return redirect(url_for('patients'))

@app.route('/appointments')
@login_required
def appointments():
    data = db.get_all_appointments()
    patients = db.get_all_patients()
    return render_template('appointments.html', appointments=data,
                           patients=patients, user=session['user'])

@app.route('/appointments/add', methods=['POST'])
@login_required
def add_appointment():
    db.add_appointment(
        request.form['patient_id'], request.form['doctor'],
        request.form['department'], request.form['date'],
        request.form['time'], request.form.get('notes','')
    )
    flash("Appointment booked!")
    return redirect(url_for('appointments'))

@app.route('/appointments/delete/<int:aid>', methods=['POST'])
@login_required
def delete_appointment(aid):
    db.delete_appointment(aid)
    return redirect(url_for('appointments'))

# ── REST API ──────────────────────────────────────────────
@app.route('/api/stats')
@login_required
def api_stats():
    return jsonify(db.get_stats())

@app.route('/api/patients')
@login_required
def api_patients():
    return jsonify([dict(id=p[0],name=p[1],age=p[2],gender=p[3],
                         phone=p[4],address=p[5],disease=p[6])
                    for p in db.get_all_patients()])

@app.route('/api/appointments')
@login_required
def api_appointments():
    return jsonify([dict(id=a[0],patient=a[2],doctor=a[3],
                         department=a[4],date=a[5],time=a[6],notes=a[7])
                    for a in db.get_all_appointments()])

@app.route('/api/chart/patients-per-day')
@login_required
def api_chart_patients():
    return jsonify(db.patients_per_day())

@app.route('/api/chart/appointments-per-dept')
@login_required
def api_chart_dept():
    return jsonify(db.appointments_per_dept())

if __name__ == '__main__':
    app.run(debug=True)
