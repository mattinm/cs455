from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .views import register_blueprints

# initialize our app
app = Flask(__name__)

# create our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# register our blueprints for routing
register_blueprints(app)

@app.route('/')
def index():
    return render_template('base.html', msg='Hello, World!')