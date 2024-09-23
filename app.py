from flask import Flask, request, jsonify
from models import db, Student
import os
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, BadRequest

app = Flask(__name__)

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for Flask application. Set the environment variable before running the app.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and migration tool
db.init_app(app)
migrate = Migrate(app, db)

# Custom error handler for 404 - Not Found
@app.errorhandler(NotFound)
def resource_not_found(e):
    return jsonify({'error': 'Resource not found', 'message': str(e)}), 404

# Custom error handler for 400 - Bad Request
@app.errorhandler(BadRequest)
def bad_request(e):
    return jsonify({'error': 'Bad request', 'message': str(e)}), 400

# Generic error handler for 500 - Internal Server Error
@app.errorhandler(Exception)
def internal_server_error(e):
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500

# Routes
@app.route('/api/v1/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'age': s.age, 'grade': s.grade} for s in students])

@app.route('/api/v1/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({'id': student.id, 'name': student.name, 'age': student.age, 'grade': student.grade})

@app.route('/api/v1/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Handle missing fields in the request
    if not all(k in data for k in ('name', 'age', 'grade')):
        raise BadRequest('Missing required fields: name, age, or grade')
    
    new_student = Student(name=data['name'], age=data['age'], grade=data['grade'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully!'}), 201

@app.route('/api/v1/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()

    if not data:
        raise BadRequest('Request body cannot be empty')

    # Handle missing fields in the request
    if not all(k in data for k in ('name', 'age', 'grade')):
        raise BadRequest('Missing required fields: name, age, or grade')

    student.name = data['name']
    student.age = data['age']
    student.grade = data['grade']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully!'})

@app.route('/api/v1/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully!'})

@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'API is healthy!'})

if __name__ == '__main__':
    app.run(debug=True)