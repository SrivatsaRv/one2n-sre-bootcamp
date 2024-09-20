import os
import logging
import warnings
from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db, Student
from dotenv import load_dotenv
from sqlalchemy.exc import LegacyAPIWarning

# Suppress SQLAlchemy LegacyAPIWarning
warnings.filterwarnings("ignore", category=LegacyAPIWarning)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the database using the DATABASE_URL environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and setup migration object
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Set up logging to both console and file
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler()  # Console handler
file_handler = logging.FileHandler('app.log')  # File handler

# Set log format
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Create the database tables when the app starts
#with app.app_context():
#   db.create_all()

# Healthcheck endpoint
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    logger.info("Healthcheck requested")
    return jsonify({"status": "healthy"}), 200

# Get all students
@app.route('/api/v1/students', methods=['GET'])
def get_students():
    logger.info("Fetching all students")
    students = Student.query.all()
    students_list = [{"id": student.id, "name": student.name, "age": student.age, "course": student.course} for student in students]
    return jsonify(students_list), 200

# Get a single student by ID
@app.route('/api/v1/students/<int:id>', methods=['GET'])
def get_student(id):
    logger.info(f"Fetching student with ID: {id}")
    student = db.session.get(Student, id)
    if student is None:
        logger.warning(f"Student with ID {id} not found")
        abort(404, description="Student not found")
    return jsonify({"id": student.id, "name": student.name, "age": student.age, "course": student.course}), 200

# Create a new student
@app.route('/api/v1/students', methods=['POST'])
def create_student():
    data = request.json
    if not data or not 'name' in data or not 'age' in data or not 'course' in data:
        logger.error("Invalid student data received for creation")
        abort(400, description="Invalid data")

    new_student = Student(name=data['name'], age=data['age'], course=data['course'])
    db.session.add(new_student)
    db.session.commit()
    logger.info(f"Student created: {new_student.name}")
    return jsonify({"message": "Student created successfully", "id": new_student.id}), 201

# Update student information
@app.route('/api/v1/students/<int:id>', methods=['PUT'])
def update_student(id):
    logger.info(f"Updating student with ID: {id}")
    student = db.session.get(Student, id)
    if student is None:
        logger.warning(f"Student with ID {id} not found for update")
        abort(404, description="Student not found")

    data = request.json
    student.name = data.get('name', student.name)
    student.age = data.get('age', student.age)
    student.course = data.get('course', student.course)

    db.session.commit()
    logger.info(f"Student updated: {student.name}")
    return jsonify({"message": "Student updated successfully"}), 200

# Delete a student
@app.route('/api/v1/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    logger.info(f"Deleting student with ID: {id}")
    student = db.session.get(Student, id)
    if student is None:
        logger.warning(f"Student with ID {id} not found for deletion")
        abort(404, description="Student not found")

    db.session.delete(student)
    db.session.commit()
    logger.info(f"Student with ID {id} deleted successfully")
    return jsonify({"message": "Student deleted successfully"}), 200

# Error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    logger.error(f"Error 404: {error}")
    return jsonify({"error": str(error)}), 404

# Error handler for 400 errors (bad requests)
@app.errorhandler(400)
def bad_request(error):
    logger.error(f"Error 400: {error}")
    return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True)