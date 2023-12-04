"""Seed file to make sample data for pets db."""

from models import Pet, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Pet.query.delete()

# Add pets
whiskey = Pet(name='Whiskey', species="dog")
bowser = Pet(name='Bowser', species="dog", hunger=10)
spike = Pet(name='Spike', species="porcupine")

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()