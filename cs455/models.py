from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    ssn = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=False)
    first_name = db.Column(db.String(16), nullable=False)
    middle_initial = db.Column(db.String(3))
    last_name = db.Column(db.String(16), nullable=False)
    street = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)

class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
class Employee(db.Model):
    __tablename__ = 'employee'
    ssn = db.Column(db.Integer, db.ForeignKey('user.ssn'), primary_key=True, nullable=False, autoincrement=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User')
    
class Specialty(db.Model):
    __tablename__ = 'specialty'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
class Doctor(db.Model):
    __tablename__ = 'doctor'
    ssn = db.Column(db.Integer, db.ForeignKey('employee.ssn'), primary_key=True, nullable=False, autoincrement=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'), nullable=False)
    
    employee = db.relationship('Employee')
    specialty = db.relationship('Specialty', backref=db.backref('doctors', lazy='dynamic'))
    
class Patient(db.Model):
    __tablename__ = 'patient'
    ssn = db.Column(db.Integer, db.ForeignKey('user.ssn'), primary_key=True, nullable=False, autoincrement=False)
    doctor_ssn = db.Column(db.Integer, db.ForeignKey('doctor.ssn'), nullable=False)
    
    doctor = db.relationship('Doctor', backref=db.backref('patients', lazy='dynamic'))
    
class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_ssn = db.Column(db.Integer, db.ForeignKey('patient.ssn'), nullable=False)
    doctor_ssn = db.Column(db.Integer, db.ForeignKey('doctor.ssn'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(250), nullable=False)
    notes = db.Column(db.String(250), nullable=False)
    checkin = db.Column(db.Boolean, default=False, nullable=False)
    
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy='dynamic'))
    doctor = db.relationship('Doctor')
    
class LabTest(db.Model):
    __tablename__ = 'lab_test'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_ssn = db.Column(db.Integer, db.ForeignKey('patient.ssn'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    result = db.Column(db.String(50), nullable=False)
    
    patient = db.relationship('Patient', backref=db.backref('lab_tests', lazy='dynamic'))
    
class Drug(db.Model):
    __tablename__ = 'drug'
    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    formula = db.Column(db.String(100), nullable=False, unique=True)
    db.base_price = db.Column(db.Float, nullable=False)
    trade_name = db.Column(db.String(50), nullable=False, unique=True)

class Prescription(db.Model):
    __tablename__ = 'prescription'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_ssn = db.Column(db.Integer, db.ForeignKey('patient.ssn'), nullable=False)
    doctor_ssn = db.Column(db.Integer, db.ForeignKey('doctor.ssn'), nullable=False)
    drug_number = db.Column(db.Integer, db.ForeignKey('drug.number'), nullable=False)
    dosage = db.Column(db.Integer, nullable=False)
    dosage_unit = db.Column(db.String(10), nullable=False)
    dosage_count = db.Column(db.Integer, nullable=False)
    per_day = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    refills = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    
    patient = db.relationship('Patient', backref=db.backref('prescriptions', lazy='dynamic'))
    doctor = db.relationship('Doctor')
    drug = db.relationship('Drug')
    
class Dispensary(db.Model):
    __tablename__ = 'dispensary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    
    prescription = db.relationship('Prescription')