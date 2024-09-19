from flask import Flask, jsonify, request, abort
from models import db, Student

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create the database tables manually when the app starts
with app.app_context():
    db.create_all()

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    students_list = [{"id": student.id, "name": student.name, "age": student.age, "course": student.course} for student in students]
    return jsonify(students_list)

# Get a single student by ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if student is None:
        abort(404, description="Student not found")
    return jsonify({"id": student.id, "name": student.name, "age": student.age, "course": student.course})

# Update student information
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if student is None:
        abort(404, description="Student not found")

    data = request.json
    student.name = data.get('name', student.name)
    student.age = data.get('age', student.age)
    student.course = data.get('course', student.course)

    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

# Delete a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student is None:
        abort(404, description="Student not found")

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})


@app.route('/healthcheck',methods=['GET'])
def get_healthcheck():
    return "API Server is Healthy and Running",200

# Error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

if __name__ == '__main__':
    app.run(debug=True)
