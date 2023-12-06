from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_wtforms_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()


class SnackViewsTestCase(TestCase):
    """Tests for views for Snacks."""

    def test_snack_add_form(self):
        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form id="snack-add-form"', html)

    def test_snack_add(self):
        with app.test_client() as client:
            d = {"name": "Test2", "price": 2}
            resp = client.post("/add", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Added Test2 at 2", html)


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Make demo data."""

        User.query.delete()

        user = User(name="Test User", email="test@test.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_user_edit_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<form", html)

    def test_user_edit(self):
        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/edit",
                data={'name': 'Test2', 'email': "test2@test.com"},
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"User {self.user_id} updated!", html)

            user = User.query.get(self.user_id)
            self.assertEquals(user.name, "Test2")
            self.assertEquals(user.email, "test2@test.com")

    def test_user_edit_form_fail(self):
        with app.test_client() as client:
            # add w/ invalid email
            resp = client.post(
                f"/users/{self.user_id}/edit",
                data={'name': 'Test3', 'email': 'not-an-email'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<form", html)
            self.assertNotIn("updated!", html)
