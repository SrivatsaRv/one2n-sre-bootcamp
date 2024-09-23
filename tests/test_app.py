import unittest
import json
from app import app, db
from models import Student

class StudentApiTestCase(unittest.TestCase):
    
    def setUp(self):
        # Setup the test client and configure testing flag
        self.app = app.test_client()
        self.app.testing = True

        # Create an in-memory SQLite database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

        # Add a sample student for testing
        self.sample_student = Student(name="John Doe", age=20, grade="A")
        db.session.add(self.sample_student)
        db.session.commit()

    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()

    # Test /api/v1/healthcheck
    def test_healthcheck(self):
        response = self.app.get('/api/v1/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertIn('OK', response.get_data(as_text=True))

    # Test /api/v1/students [GET] - Get all students
    def test_get_all_students(self):
        response = self.app.get('/api/v1/students')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)  # We added one student in setUp
        self.assertEqual(data[0]['name'], "John Doe")

    # Test /api/v1/students/<id> [GET] - Get a student by ID
    def test_get_student_by_id(self):
        response = self.app.get(f'/api/v1/students/{self.sample_student.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], "John Doe")

    # Test /api/v1/students [POST] - Add a new student
    def test_add_student(self):
        new_student = {'name': 'Jane Doe', 'age': 22, 'grade': 'B'}
        response = self.app.post('/api/v1/students', data=json.dumps(new_student), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Student added successfully!')

    # Test /api/v1/students/<id> [PUT] - Update student information
    def test_update_student(self):
        update_data = {'name': 'John Updated', 'age': 21, 'grade': 'A+'}
        response = self.app.put(f'/api/v1/students/{self.sample_student.id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Student updated successfully!')

        # Verify the update
        updated_student = Student.query.get(self.sample_student.id)
        self.assertEqual(updated_student.name, 'John Updated')

    # Test /api/v1/students/<id> [DELETE] - Delete a student
    def test_delete_student(self):
        response = self.app.delete(f'/api/v1/students/{self.sample_student.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Student deleted successfully!')

        # Verify the student is actually deleted
        deleted_student = Student.query.get(self.sample_student.id)
        self.assertIsNone(deleted_student)

if __name__ == '__main__':
    unittest.main()