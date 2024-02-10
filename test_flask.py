from unittest import TestCase
from models import db, User, connect_db
from app import create_app

class UserViewsTestCase(TestCase):

    def setUp(self):
        # Create a Flask app with testing config
        self.app = create_app("blogly_db_test", testing=True)
        
        # Establish app context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Connect to the database
        connect_db(self.app)
        
        # Drop all tables (if any)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Add test data
        user = User(first_name='Test', last_name="Case")
        db.session.add(user)
        db.session.commit()
        
        # Save user ID for later use
        self.user_id = user.id

    def tearDown(self):
        # Rollback any changes made to the database
        db.session.rollback()
        
        # Pop the app context
        self.app_context.pop()

    def test_redirect_to_users(self):
        with self.app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.headers["Location"], "/users")

    def test_users_list(self):
        with self.app.test_client() as client:
            resp = client.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Test Case", html)

    def test_show_user_details(self):
        with self.app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<h5 class=\"card-title\">Test Case</h5>", html)

    def test_add_user(self):
        with self.app.test_client() as client:
            data = {"firstName": "Test2", "lastName": "Case2", "imageUrl": "https/ggoogle.jpeg"}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2 Case2", html)

    def test_delete_user(self):
        with self.app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn("Test Case", html)
