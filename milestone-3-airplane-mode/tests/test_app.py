import pytest
from app import app, db
from models import Student
from flask import json
import os
from sqlalchemy import text

# Fixtures for setting up a separate test database
@pytest.fixture
def client():
    # Use test database from the environment variable
    test_db_url = os.getenv('DATABASE_URL_TEST_CONTAINER')

    if not test_db_url:
        raise ValueError("DATABASE_URL_TEST_CONTAINER not set in the environment variables")

    app.config['SQLALCHEMY_DATABASE_URI'] = test_db_url
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            # Ensure the test database is selected and reset
            with db.engine.connect() as connection:
                connection.execute(text("USE test_student_db"))
            
            # Drop and recreate all tables to reset the database for each test
            db.drop_all()
            db.create_all()

        yield client

        # Drop all tables after the tests (optional, if you want to reset it afterward)
        with app.app_context():
            db.drop_all()


# Test Health Check Endpoint
def test_healthcheck(client):
    response = client.get('/api/v1/healthcheck')
    assert response.status_code == 200
    assert response.json == {'status': 'API is healthy!'}


# Test GET All Students (Initially no students)
def test_get_students_empty(client):
    response = client.get('/api/v1/students')
    assert response.status_code == 200
    assert response.json == []  # No students initially


# Test POST a New Student
def test_add_student(client):
    data = {'name': 'John Doe', 'age': 20, 'grade': 'A'}
    response = client.post('/api/v1/students', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'] == 'Student added successfully!'

    # Verify the student was added
    get_response = client.get('/api/v1/students')
    assert get_response.status_code == 200
    assert len(get_response.json) == 1  # 1 student added


# Test GET a Single Student
def test_get_student(client):
    # Add a student within the application context
    with app.app_context():
        new_student = Student(name='Jane Doe', age=22, grade='B')
        db.session.add(new_student)
        db.session.commit()

        # Re-query the student using session.get() to avoid warnings
        queried_student = db.session.get(Student, new_student.id)

    # Retrieve the student by ID
    response = client.get(f'/api/v1/students/{queried_student.id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Jane Doe'
    assert response.json['age'] == 22
    assert response.json['grade'] == 'B'


# Test PUT Update Student
def test_update_student(client):
    # Add a student within the application context
    with app.app_context():
        new_student = Student(name='John Smith', age=25, grade='C')
        db.session.add(new_student)
        db.session.commit()

        # Re-query the student using session.get()
        queried_student = db.session.get(Student, new_student.id)

    # Update the student's details
    update_data = {'name': 'John Smith', 'age': 26, 'grade': 'B'}
    response = client.put(f'/api/v1/students/{queried_student.id}', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'Student updated successfully!'

    # Verify the changes
    updated_response = client.get(f'/api/v1/students/{queried_student.id}')
    assert updated_response.status_code == 200
    assert updated_response.json['age'] == 26
    assert updated_response.json['grade'] == 'B'


# Test DELETE a Student
def test_delete_student(client):
    # Add a student within the application context
    with app.app_context():
        new_student = Student(name='Jane Smith', age=23, grade='A')
        db.session.add(new_student)
        db.session.commit()

        # Re-query the student using session.get()
        queried_student = db.session.get(Student, new_student.id)

    # Delete the student
    response = client.delete(f'/api/v1/students/{queried_student.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Student deleted successfully!'

    # Verify the student is gone
    get_response = client.get(f'/api/v1/students/{queried_student.id}')
    assert get_response.status_code == 404


# Test GET a Student Not Found (Error Handling)
def test_get_student_not_found(client):
    response = client.get('/api/v1/students/999')  # Student with ID 999 doesn't exist
    assert response.status_code == 404
    assert response.json['error'] == 'Resource not found'


# Test POST Student with Missing Fields (Error Handling)
def test_add_student_missing_fields(client):
    data = {'name': 'Incomplete Student'}
    response = client.post('/api/v1/students', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Bad request'
    assert 'message' in response.json
    assert 'Missing required fields' in response.json['message']