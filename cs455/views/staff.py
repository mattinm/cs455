from flask import Blueprint, render_template

staff = Blueprint('staff', __name__)

@staff.route('/')
@staff.route('/<staff_id>')
def index(staff_id=None):
    return render_template('staff/staff.html')