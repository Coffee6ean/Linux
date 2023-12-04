from unittest import TestCase

from app import app
from models import db, Pet

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class PetModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing pets."""
        Pet.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_greet(self): 
        pet = Pet(name="TestPet", species="dog", hunger=10)
        self.assertEquals(pet.greet(), "Hi, I am TestPet the dog")

    def test_feed(self):
        pet = Pet(name="TestPet", species="dog", hunger=10)
        pet.feed(5)
        self.assertEquals(pet.hunger, 5)

        pet.feed(999)
        self.assertEquals(pet.hunger, 0)

    def test_get_by_species(self):
        pet = Pet(name="TestPet", species="dog", hunger=10)
        db.session.add(pet)
        db.session.commit()

        dogs = Pet.get_by_species('dog')
        self.assertEquals(dogs, [pet])

