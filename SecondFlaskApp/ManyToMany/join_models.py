from flask_sqlalchemy import SQLAlchemy

# import sys, os
# # Add the path to the directory containing models.py to sys.path
# sys.path.append("../")
# from Associations.app import db

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS:
class Department(db.Model):
    """Department Model"""

    __tablename__ = 'departments'

    dept_code = db.Column(db.Text, primary_key=True)
    dept_name = db.Column(db.Text, nullable=False, unique=True)
    phone = db.Column(db.Text)

    def __repr__(self):
        return f"<Department {self.dept_code} {self.dept_name} {self.phone}>"
    
    #employees = db.relationship('Employee')

class Employee(db.Model):
    """Employee Model"""

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    state = db.Column(db.Text, nullable=False, default='CA')
    dept_code = db.Column(db.Text, db.ForeignKey('departments.dept_code'))

    # Magic line
    # Sets up a dept attribute on each instance of Employee
    # SQLA will populate it with data from the departments table automatically
    dept = db.relationship('Department', backref='employees')

    # Relationships
    # assignments = db.relationship('EmployeeProject', backref='employee')

    # 'Through' Relationships
    projects = db.relationship('Project', 
                               secondary='employee_projects', backref='employees')

    def __repr__(self):
        return f"<Employee {self.name} {self.state} {self.dept_code}>"
    
class Project(db.Model):
    """Project Model"""

    __tablename__ = 'projects'

    proj_code = db.Column(db.Text, primary_key=True)
    proj_name = db.Column(db.Text, nullable=False, unique=True)

    assignments = db.relationship('EmployeeProject', backref='project')

class EmployeeProject(db.Model):
    """Employee-Project Model"""
    __tablename__ = 'employee_projects'

    emp_id = db.Column(db.Integer, 
            db.ForeignKey('employees.id'), primary_key=True)
    proj_code = db.Column(db.Text, 
            db.ForeignKey('projects.proj_code'), primary_key=True)
    
    role = db.Column(db.Text)
    
def get_directory():
    all_emps = Employee.query.all()

    for emp in all_emps:
        if emp.dept is not None:
            print(emp.name, emp.dept.dept_name, emp.dept.phone)
        else:
            print(emp.name)
    
def get_directory_join():
    directory = db.session.query(
        Employee.name, Department.dept_name, Department.phone
        ).join(Department).all()
    
    for name, dept, phone in directory:
        print(name, dept, phone)

def get_directory_join_class():
    directory = db.session.query(
        Employee, Department
        ).join(Department).all()
    
    for emp, dept in directory:
        print(emp.name, dept.dept_name, dept.phone)

def get_directory_outerjoin_dept():
    directory = db.session.query(
        Employee.name, Department.dept_name, Department.phone
        ).outerjoin(Department).all()
    
    for name, dept, phone in directory:
        print(name, dept, phone)

def get_directory_outerjoin_emp():
    directory = db.session.query(
        Employee.name, Department.dept_name, Department.phone
        ).outerjoin(Employee).all()
    
    for name, dept, phone in directory:
        print(name, dept, phone)