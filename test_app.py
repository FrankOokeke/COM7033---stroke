import unittest
from app import app
from db_handler import DBHandler

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True
        self.db_handler = DBHandler()

    def test_register_user(self):
        response = self.app.post('/register', data={
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_login_user(self):
        response = self.app.post('/login', data={
            'username': 'admin',
            'password': 'admin_password'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_access_admin(self):
        with self.app.session_transaction() as session:
            session['username'] = 'admin'
            session['role'] = 'admin'
        response = self.app.get('/admin/patients')
        self.assertEqual(response.status_code, 200)  # Admin page is accessible

    def test_add_patient(self):
        with self.app.session_transaction() as session:
            session['username'] = 'admin'
            session['role'] = 'admin'
        response = self.app.post('/admin/patients', data={
            'id': 123,
            'gender': 'Male',
            'age': 45,
            'hypertension': 0,
            'heart_disease': 0,
            'ever_married': 'Yes',
            'work_type': 'Private',
            'Residence_type': 'Urban',
            'avg_glucose_level': 120.5,
            'bmi': 25.3,
            'smoking_status': 'Never smoked'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

if __name__ == '__main__':
    unittest.main()