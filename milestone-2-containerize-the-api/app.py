import logging
from flask import Flask, request, jsonify
from models import db, Student
import os
from flask_migrate import Migrate
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Configuration using environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for Flask application. Set the environment variable before running the app.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and migration tool
db.init_app(app)
migrate = Migrate(app, db)

# Disable the default werkzeug logger
log = logging.getLogger('werkzeug')
log.disabled = True

# Set up logging to file only (disable console output)
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Application has started.')

# Custom error handler for 404 - Not Found
@app.errorhandler(404)
def resource_not_found(e):
    logging.error(f"Resource not found: {request.url}")
    return jsonify({'error': 'Resource not found'}), 404

# Custom error handler for 400 - Bad Request
@app.errorhandler(400)
def bad_request(e):
    logging.error(f"Bad request: {request.url} - {request.data}")
    return jsonify({'error': 'Bad request', 'message': str(e)}), 400

# Generic error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Server error: {str(e)}")
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500

# Routes
@app.route('/api/v1/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    logging.info('Fetched all students.')
    return jsonify([{'id': s.id, 'name': s.name, 'age': s.age, 'grade': s.grade} for s in students])

@app.route('/api/v1/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    logging.info(f"Fetched student with ID {id}.")
    return jsonify({'id': student.id, 'name': student.name, 'age': student.age, 'grade': student.grade})

@app.route('/api/v1/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Handle missing fields in the request
    if not all(k in data for k in ('name', 'age', 'grade')):
        logging.warning(f"Bad request - Missing fields in POST data: {data}")
        return bad_request('Missing required fields: name, age, or grade')
    
    new_student = Student(name=data['name'], age=data['age'], grade=data['grade'])
    db.session.add(new_student)
    db.session.commit()
    logging.info(f"Added new student: {data['name']}.")
    return jsonify({'message': 'Student added successfully!'}), 201

@app.route('/api/v1/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()

    if not data:
        logging.warning(f"Bad request - No data in PUT request for student ID {id}")
        return bad_request('Request body cannot be empty')

    student.name = data['name']
    student.age = data['age']
    student.grade = data['grade']
    db.session.commit()
    logging.info(f"Updated student with ID {id}.")
    return jsonify({'message': 'Student updated successfully!'})

@app.route('/api/v1/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    logging.info(f"Deleted student with ID {id}.")
    return jsonify({'message': 'Student deleted successfully!'})

@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    logging.info('Health check endpoint called.')
    return jsonify({'status': 'API is healthy!'})

if __name__ == '__main__':
    logging.info('Starting the Flask application...')
    app.run(debug=True, host='0.0.0.0', port=5000)