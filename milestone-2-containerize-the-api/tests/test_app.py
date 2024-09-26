import unittest
import json
from app import app, db
from models import Student
import os
from dotenv import load_dotenv  # Load environment variables

# Load environment variables from .env
load_dotenv()

class StudentApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask test client and configure the testing flag
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def setUp(self):
        # Ensure the app uses the MySQL test database, not the production database
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DB_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Clean up the test database before each test
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Only drops the test database
            db.create_all()

            # Insert a sample student for testing
            sample_student = Student(name="John Doe", age=20, grade="A")
            db.session.add(sample_student)
            db.session.commit()

    def tearDown(self):
        # Clean up the test database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test /api/v1/healthcheck
    def test_healthcheck(self):
        response = self.client.get('/api/v1/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertIn('API is healthy', response.get_data(as_text=True))

    # Test /api/v1/students [GET] - Get all students
    def test_get_all_students(self):
        response = self.client.get('/api/v1/students')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)  # We added one student in setUp
        self.assertEqual(data[0]['name'], "John Doe")

    # Test /api/v1/students/<id> [GET] - Get a student by ID
    def test_get_student_by_id(self):
        response = self.client.get('/api/v1/students/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], "John Doe")

    # Test /api/v1/students [POST] - Add a new student
    def test_add_student(self):
        new_student = {'name': 'Jane Doe', 'age': 22, 'grade': 'B'}
        response = self.client.post('/api/v1/students', data=json.dumps(new_student), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Student added successfully!')

    # Test /api/v1/students/<id> [PUT] - Update student information
    def test_update_student(self):
        update_data = {'name': 'John Updated', 'age': 21, 'grade': 'A+'}
        response = self.client.put('/api/v1/students/1', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Student updated successfully!')

    # Test /api/v1/students/<id> [DELETE] - Delete a student
    def test_delete_student(self):
        response = self.client.delete('/api/v1/students/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Student deleted successfully!')

if __name__ == '__main__':
    unittest.main()