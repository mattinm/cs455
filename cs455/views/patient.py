from flask import Blueprint, render_template

patient = Blueprint('patient', __name__, template_folder='templates')

@patient.route('/')
@patient.route('/<patient_id>')
def index(patient_id=None):
    return render_template('patient/patient.html')