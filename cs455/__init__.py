from flask import Flask, render_template
from .views import register_blueprints
from .database import db_session

app = Flask(__name__)

# register our blueprints for routing
register_blueprints(app)

# teardown the database automatically
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return render_template('base.html', msg='Hello, World!')