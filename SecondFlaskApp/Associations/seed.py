"""Seed file to make sample data for db."""

# from models import Department, Employee, db

import sys, os
sys.path.append("../")
from ManyToMany.join_models import Department, Employee, Project, EmployeeProject, db

from app import app

# Create all tables
db.drop_all()
db.create_all()

# d1 = Department(dept_code="mktg", dept_name="Marketing", phone="897-9999")
# d2 = Department(dept_code="acct", dept_name="Accounting", phone="111-5429")
# d3 = Department(dept_code="r&d", dept_name="Research and Development", phone="908-7878")
# d4 = Department(dept_code="it", dept_name="Information Technology", phone="888-4562")
# d5 = Department(dept_code="sales", dept_name="Sales", phone="225-6912")
# 
# emp1 = Employee(name="River Bottom", state="NY", dept_code="mktg")
# emp2 = Employee(name="Summer Winter", state="OR", dept_code="mktg")
# emp3 = Employee(name="Joaquin Phoenix", dept_code="acct")
# emp4 = Employee(name="Octavia Spencer", dept_code="r&d")
# emp5 = Employee(name="Larry David", dept_code="r&d", state="NY")
# emp6 = Employee(name="Kurt Cobain", dept_code="it", state="WA")
# emp7 = Employee(name="Rain Phoenix", dept_code="it")
# 
# db.session.add_all([d1, d2, d3, d4, d5])
# db.session.add_all([emp1, emp2, emp3, emp4, emp5, emp6, emp7])
# 
# db.session.commit()

EmployeeProject.query.delete()
Employee.query.delete()
Department.query.delete()
Project.query.delete()

# Add sample employees and departments
df = Department(dept_code='fin', dept_name='Finance', phone='555-1000')
dl = Department(dept_code='legal', dept_name='Legal', phone='555-2222')
dm = Department(dept_code='mktg', dept_name='Marketing', phone='555-9999')

emp1 = Employee(name='Leonard', dept=dl)
emp2 = Employee(name='Liz', dept=dl)
emp3 = Employee(name='Maggie', state='DC', dept=dm)
emp4 = Employee(name='Nadine')

db.session.add_all([df, dl, dm, emp1, emp2, emp3, emp4])
db.session.commit()

pc = Project(proj_code='car', proj_name='Design Car', 
             assignments=[EmployeeProject(emp_id=emp2.id, role='Chair'),
                          EmployeeProject(emp_id=emp3.id)])
ps = Project(proj_code='server', proj_name='Deploy Server',
             assignments=[EmployeeProject(emp_id=emp2.id),
                          EmployeeProject(emp_id=emp1.id, role='Auditor')])

db.session.add_all([ps, pc])
db.session.commit()