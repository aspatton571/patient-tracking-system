from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Patient, init_db
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-key'

db.init_app(app)

@app.before_first_request
def setup():
    init_db(app)

@app.route('/')
def index():
    return redirect(url_for('patients'))

@app.route('/patients')
def patients():
    q = request.args.get('q', '').strip()
    status = request.args.get('status', '').strip()
    query = Patient.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Patient.first_name.ilike(like)) |
            (Patient.last_name.ilike(like)) |
            (Patient.mrn.ilike(like)) |
            (Patient.location.ilike(like))
        )
    if status:
        query = query.filter_by(status=status)
    data = query.order_by(Patient.updated_at.desc()).all()
    return render_template('patients_list.html', patients=data, q=q, status=status)

@app.route('/patients/new', methods=['GET', 'POST'])
def patient_new():
    if request.method == 'POST':
        form = request.form
        p = Patient(
            first_name=form.get('first_name'),
            last_name=form.get('last_name'),
            dob=form.get('dob') or None,
            mrn=form.get('mrn'),
            status=form.get('status') or 'Registered',
            location=form.get('location'),
            notes=form.get('notes')
        )
        db.session.add(p)
        db.session.commit()
        flash('Patient added')
        return redirect(url_for('patients'))
    return render_template('patient_form.html', patient=None)

@app.route('/patients/<int:pid>/edit', methods=['GET', 'POST'])
def patient_edit(pid):
    p = Patient.query.get_or_404(pid)
    if request.method == 'POST':
        form = request.form
        p.first_name = form.get('first_name')
        p.last_name = form.get('last_name')
        p.dob = form.get('dob') or None
        p.mrn = form.get('mrn')
        p.status = form.get('status') or p.status
        p.location = form.get('location')
        p.notes = form.get('notes')
        p.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Patient updated')
        return redirect(url_for('patients'))
    return render_template('patient_form.html', patient=p)

@app.route('/patients/<int:pid>/discharge', methods=['POST'])
def patient_discharge(pid):
    p = Patient.query.get_or_404(pid)
    p.status = 'Discharged'
    p.updated_at = datetime.utcnow()
    db.session.commit()
    flash('Patient discharged')
    return redirect(url_for('patients'))

@app.route('/patients/<int:pid>/delete', methods=['POST'])
def patient_delete(pid):
    p = Patient.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('Patient deleted')
    return redirect(url_for('patients'))

if __name__ == '__main__':
    app.run(debug=True)
