from unittest import TestCase

from app import app
from models import db, Pet

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class PetViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        Pet.query.delete()

        pet = Pet(name="TestPet", species="dog", hunger=10)
        db.session.add(pet)
        db.session.commit()

        self.pet_id = pet.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    def test_list_pets(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestPet', html)

    def test_show_pet(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestPet</h1>', html)

    def test_add_pet(self):
        with app.test_client() as client:
            d = {"name": "TestPet2", "species": "cat", "hunger": 20}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestPet2</h2>", html)