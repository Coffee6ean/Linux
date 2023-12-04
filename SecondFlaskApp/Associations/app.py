from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
#from models import db, connect_db, Department, Employee, get_directory

import sys
# Add the path to the directory containing models.py to sys.path
sys.path.append("../")
from ManyToMany.join_models import \
    db, connect_db, Department, Employee, Project, EmployeeProject, \
    get_directory, get_directory_join, get_directory_join_class, \
    get_directory_outerjoin_dept, get_directory_outerjoin_emp

from DefiningAForm.forms import AddSnackForm

app = Flask(__name__)

# Pushing an application context to make sure the app is context-aware
# This is necessary for certain operations, such as database interactions.
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///employees_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'thousandsunny17'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

# ROUTES
@app.route("/phones")
def list_phones():
    emps = Employee.query.all()
    return render_template('phones.html', emps=emps)

@app.route("/snacks/new")
def add_snack():
    form = AddSnackForm()

    return render_template("add_snack_form.html", form=form)