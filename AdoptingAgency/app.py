from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Pet

import sys
sys.path.append("../")
from Forms.form import AddAnimalForm
app = Flask(__name__)

# Pushing an application context to make sure the app is context-aware
# This is necessary for certain operations, such as database interactions.
app.app_context().push()

# Configuration for connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_animal_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Print SQL statements to the console
app.config['SECRET_KEY'] = 'thousandSunny17'  # Secret key for session management
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Disable Flask Debug Toolbar for redirects

# Creating and initializing the SQLAlchemy instance
connect_db(app)

# Function to run before the first request
def fill_app():
    import sys
    sys.path.append("../")
    from Seeds.seed import initialize_app, seed_data
    initialize_app()
    seed_data()

fill_app()

# ROUTES
@app.route('/')
def home_page():
    pets = Pet.query.all()
    print(pets[0].photo_url)
    return render_template('home_page.html', pets=pets)

@app.route('/pets/list')
def display_pets():
    pets = Pet.query.all()
    return render_template('pets_list.html', pets=pets)

@app.route('/pets/new', methods=['GET', 'POST'])
def add_pet():
    form = AddAnimalForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo = form.photo.data
        age = form.age.data
        notes = form.notes.data
        return redirect('/pets/list')
    else:
        return render_template('add_pet_form.html', form=form)
