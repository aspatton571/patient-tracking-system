from app import app, db
from models import Patient

sample = [
    dict(first_name='Maya', last_name='Hughes', dob='1985-04-01', mrn='A1001', status='Admitted', location='ICU-2', notes='Hypertension'),
    dict(first_name='Luis', last_name='Ramirez', dob='1977-09-20', mrn='A1002', status='Registered', location='ED-3', notes='Chest pain'),
    dict(first_name='Ava', last_name='Chen', dob='1992-11-05', mrn='A1003', status='Discharged', location='Ward-5', notes='Post-op follow up'),
]

with app.app_context():
    db.create_all()
    if Patient.query.count() == 0:
        for row in sample:
            db.session.add(Patient(**row))
        db.session.commit()
        print('Seeded 3 patients.')
    else:
        print('Database already has data. No action taken.')
