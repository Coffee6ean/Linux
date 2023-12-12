"""Seed file to make sample data for db."""

import sys
sys.path.append("../")
from models import Pet, db
from app import app

def initialize_app():
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    Pet.query.delete()

def seed_data():
    # Add pets
    pet1 = Pet(
        name='Ragu', 
        species='Dog', 
        photo_url='https://images.unsplash.com/photo-1623249670310-7b7c39de2d07?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDh8fHB1Z3xlbnwwfHwwfHx8MA%3D%3D', 
        age=4, 
        notes='Very chunky and a beautiful girl'
    )
    pet2 = Pet(
        name='Carlotita', 
        species='Dog', 
        photo_url='https://images.unsplash.com/photo-1453227588063-bb302b62f50b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cHVnfGVufDB8fDB8fHww', 
        age=2, 
        notes='Her royal highness pug version'
    )
    pet3 = Pet(
        name='Albondiga', 
        species='Dog', 
        photo_url='https://images.unsplash.com/photo-1529927066849-79b791a69825?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjJ8fHB1Z3xlbnwwfHwwfHx8MA%3D%3D', 
        notes='Fat, cute and kinda of a pig', 
        available=False
    )
    pet4 = Pet(
        name='Kireina', 
        species='Dog', 
        photo_url='https://images.unsplash.com/photo-1581351877917-fd4b965ead15?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjF8fHNjaG5hdXplcnxlbnwwfHwwfHx8MA%3D%3D', 
        age=15, 
        notes='The most beautiful, intelligent and loveliest lady ever...I miss you', 
        available=False
    )

    # Add new objects to session, so they'll persist
    db.session.add_all([pet1, pet2, pet3, pet4])

    # Commit session
    db.session.commit()

# Run before the first request
initialize_app()
seed_data()
