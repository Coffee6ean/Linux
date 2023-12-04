from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import db, connect_db, Pet

app = Flask(__name__)

# Pushing an application context to make sure the app is context-aware
# This is necessary for certain operations, such as database interactions.
app.app_context().push()

# Configuration for connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Print SQL statements to the console
app.config['SECRET_KEY'] = 'thousandSunny17'  # Secret key for session management
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Disable Flask Debug Toolbar for redirects

# Creating and initializing the SQLAlchemy instance
connect_db(app)

# Route to the home page
@app.route('/')
def home_page():
    """Shows list of all pets in db"""
    pets = Pet.query.all()
    return render_template('list.html', pets=pets)

@app.route('/', methods=['POST'])
def create_pet():
    name = request.form.get('name')
    species = request.form.get('species')
    hunger = request.form.get('hunger')
    hunger = int(hunger) if hunger else None

    new_pet = Pet(name=name, species=species, hunger=hunger)
    db.session.add(new_pet)
    db.session.commit()

    return redirect(f"/{new_pet.id}")

@app.route('/<int:pet_id>')
def show_pet(pet_id):
    """Show details about single pet"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template('details.html', pet=pet)

@app.route("/species/<species_id>")
def show_pets_by_species(species_id):
    pets = Pet.get_by_species(species_id)
    return render_template("species.html", pets=pets, species=species_id)