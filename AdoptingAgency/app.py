from flask import Flask, request, redirect, \
                    render_template, flash, url_for, \
                    jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Pet
from Keys.secrets import APP_KEY

import sys
sys.path.append("../")
from Forms.form import AddPetForm, EditPetForm
app = Flask(__name__)

# Pushing an application context to make sure the app is context-aware
# This is necessary for certain operations, such as database interactions.
app.app_context().push()

# Configuration for connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_animal_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Print SQL statements to the console
app.config['SECRET_KEY'] = APP_KEY  # Secret key for session management
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Disable Flask Debug Toolbar for redirects

# Creating and initializing the SQLAlchemy instance
connect_db(app)

# ROUTES
@app.route('/')
def home_page():
    pets = Pet.query.all()
    print(pets[0].photo_url)
    return render_template('home_page.html', pets=pets)

@app.route('/pets/list')
def list_pets():
    pets = Pet.query.all()
    return render_template('pets_list.html', pets=pets)

@app.route('/pets/new', methods=['GET', 'POST'])
def add_pet():
    """Add new Pet."""
    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        # new_pet = Pet(name=form.name.data, age=form.age.data, ...)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect('/pets/list')
    else:
        return render_template('add_pet_form.html', form=form)
    
@app.route('/pets/<int:id>', methods=['GET', 'POST'])
def get_pet(id):
    """Edit existing Pet."""
    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))
    else:
        return render_template("edit_pet_form.html", form=form, pet=pet)

@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)

