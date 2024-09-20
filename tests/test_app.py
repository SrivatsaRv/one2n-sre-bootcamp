import pytest
import warnings
from app import app, db
from models import Student

# Suppress DeprecationWarnings (such as from Werkzeug)
warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture
def client():
    """Set up the Flask test client for testing."""
    app.config['TESTING'] = True  # Enable testing mode
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Ensure the tables are created
            # Insert some sample student records for testing
            student1 = Student(name="John Doe", age=22, course="Physics")
            student2 = Student(name="Jane Doe", age=23, course="Math")
            db.session.add_all([student1, student2])
            db.session.commit()
            yield client
        db.drop_all()  # Clean up the database after each test

def test_healthcheck(client):
    """Test the /healthcheck endpoint"""
    rv = client.get('/healthcheck')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == "healthy"

def test_get_all_students(client):
    """Test retrieving all students"""
    rv = client.get('/api/v1/students')
    assert rv.status_code == 200
    students = rv.get_json()
    # Verify that some students exist (adjust if you know how many)
    assert len(students) > 0

def test_get_student_by_id(client):
    """Test retrieving a student by ID"""
    rv = client.get('/api/v1/students/1')  # Test with student ID 1
    assert rv.status_code == 200
    student = rv.get_json()
    assert student['id'] == 1
    assert 'name' in student  # Ensure 'name' field exists

def test_create_student(client):
    """Test creating a new student"""
    new_student = {
        "name": "New Student",
        "age": 22,
        "course": "Physics"
    }
    rv = client.post('/api/v1/students', json=new_student)
    assert rv.status_code == 201
    response_data = rv.get_json()
    assert response_data['message'] == "Student created successfully"
    assert 'id' in response_data  # New student should have an ID

def test_update_student(client):
    """Test updating a student's record by ID"""
    updated_data = {
        "name": "Updated Student",
        "age": 23,
        "course": "Math"
    }
    rv = client.put('/api/v1/students/1', json=updated_data)  # Update student with ID 1
    assert rv.status_code == 200
    assert b"Student updated successfully" in rv.data

    # Verify the update by fetching the student again
    rv = client.get('/api/v1/students/1')
    student = rv.get_json()
    assert student['name'] == "Updated Student"
    assert student['age'] == 23
    assert student['course'] == "Math"

def test_delete_student(client):
    """Test deleting a student by ID"""
    rv = client.delete('/api/v1/students/1')
    assert rv.status_code == 200
    assert b"Student deleted successfully" in rv.data

    # Verify the student is no longer in the database
    rv = client.get('/api/v1/students/1')
    assert rv.status_code == 404  # Student with ID 1 should no longer exist