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

from DefiningAForm.forms import AddSnackForm, NewEmployeeForm

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
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route("/phones")
def list_phones():
    """Renders directory of employees and phone numbers (from dept)"""
    emps = Employee.query.all()
    return render_template('phones.html', emps=emps)

@app.route("/snacks/new", methods=['GET', 'POST'])
def add_snack():
    print(request.form)
    form = AddSnackForm()

    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        quantity = form.quantity.data
        is_helthy = form.is_healthy.data
        flash(f"Created new snack: name is {name}, price is ${price}")
        return redirect('/')
    else:
        return render_template("add_snack_form.html", form=form)
    
@app.route('/employees/new', methods=['GET', 'POST'])
def add_employee():
    form = NewEmployeeForm()
    depts = db.session.query(Department.dept_code, Department.dept_name).all()
    form.dept_code.choices = [(dept_code, dept_name) for dept_code, dept_name in depts]

    if form.validate_on_submit():
        name = form.name.data
        state = form.state.data
        dept_code = form.dept_code.data

        emp = Employee(name=name, state=state, dept_code=dept_code)
        db.session.add(emp)
        db.session.commit()

        return redirect('/phones')
    else:
        return render_template('add_employee_form.html', form=form)