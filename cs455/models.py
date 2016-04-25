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
    
    def __init__(self, ssn, first_name, last_name, street, city, zipcode, birthday, middle_initial=None):
        self.ssn = ssn
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.street = street
        self.city = city
        self.zipcode = zipcode
        self.birthday = birthday
        
    def __repr__(self):
        return '<User %r %r>' % (self.first_name, self.last_name)
        
class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<Position %r>' % self.name
    
class Department(db.Model):
    __tablename__ = 'department'
    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    
    def __init__(self, number, name, phone_number, room):
        self.number = number
        self.name = name
        self.phone_number = phone_number
        self.room = room
        
    def __repr__(self):
        return '<Department %r>' % self.name
    
class Employee(db.Model):
    __tablename__ = 'employee'
    ssn = db.Column(db.Integer, db.ForeignKey('user.ssn'), primary_key=True, nullable=False, autoincrement=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.number'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User')
    position = db.relationship('Position', backref=db.backref('employees', lazy='dynamic'))
    department = db.relationship('Department', backref=db.backref('employees', lazy='dynamic'))
    
    def __init__(self, user, position, department, start_date):
        self.user = user
        self.position = position
        self.department = department
        self.start_date = start_date
        
    def __repr__(self):
        return '<Employee %r in %r as %r' % (self.user, self.department, self.position)
    
class Specialty(db.Model):
    __tablename__ = 'specialty'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<Specialty %r>' % self.name
    
class Doctor(db.Model):
    __tablename__ = 'doctor'
    ssn = db.Column(db.Integer, db.ForeignKey('employee.ssn'), primary_key=True, nullable=False, autoincrement=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'), nullable=False)
    
    employee = db.relationship('Employee')
    specialty = db.relationship('Specialty', backref=db.backref('doctors', lazy='dynamic'))
    
    def __init__(self, employee, specialty):
        self.employee = employee
        self.specialty = specialty
        
    def __repr__(self):
        return '<Doctor %r in %r>' % (self.employee, self.specialty)
    
class Patient(db.Model):
    __tablename__ = 'patient'
    ssn = db.Column(db.Integer, db.ForeignKey('user.ssn'), primary_key=True, nullable=False, autoincrement=False)
    doctor_ssn = db.Column(db.Integer, db.ForeignKey('doctor.ssn'), nullable=False)
    
    user = db.relationship('User')
    doctor = db.relationship('Doctor', backref=db.backref('patients', lazy='dynamic'))
    
    def __init__(self, user, doctor):
        self.user = user
        self.doctor = doctor
        
    def __repr__(self):
        return '<Patient %r with %r>' % (self.user, self.doctor)
    
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
    
    def __init__(self, patient, doctor, date, reason):
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.reason = reason
        self.notes = ''
        self.checkin = False
        
    def __repr__(self):
        return '<Appointment %r with %r on %r>' % (self.patient, self.doctor, self.date)
    
class LabTest(db.Model):
    __tablename__ = 'lab_test'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_ssn = db.Column(db.Integer, db.ForeignKey('patient.ssn'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    result = db.Column(db.String(50), nullable=False)
    
    patient = db.relationship('Patient', backref=db.backref('lab_tests', lazy='dynamic'))
    
    def __init__(self, patient, date, name):
        self.patient = patient
        self.date = date
        self.name = name
        self.result = 'Pending'
        
    def __repr__(self):
        return '<LabTest %r for %r with %r>' % (self.name, self.patient, self.result)
    
class Drug(db.Model):
    __tablename__ = 'drug'
    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    formula = db.Column(db.String(100), nullable=False, unique=True)
    base_price = db.Column(db.Float, nullable=False)
    trade_name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, number, formula, base_price, trade_name):
        self.number = number
        self.formula = formula
        self.base_price = base_price
        self.trade_name = trade_name
        
    def __repr__(self):
        return '<Drug %r>' % self.trade_name

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
    
    def __init__(self, patient, doctor, drug, dosage, dosage_unit, dosage_count, per_day, quantity, refills, date):
        self.patient = patient
        self.doctor = doctor
        self.drug = drug
        self.dosage = dosage
        self.dosage_unit = dosage_unit
        self.dosage_count = dosage_count
        self.per_day = per_day
        self.quantity = quantity
        self.refills = refills
        self.date = date
        
    def __repr__(self):
        return '<Prescription %r by %r for %r>' % (self.patient, self.doctor, self.drug)
    
class Dispensary(db.Model):
    __tablename__ = 'dispensary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    
    prescription = db.relationship('Prescription')
    
    def __init__(self, prescription, date):
        self.prescription = prescription
        self.date = date
        
    def __repr__(self):
        return '<Dispensary %r on %r>' % (self.prescription, self.date)