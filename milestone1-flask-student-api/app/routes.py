from flask import Flask, request, jsonify
from app.models import db, Student

app = Flask(__name__)
app.config.from_object('app.config.Config')
db.init_app(app)

@app.route('/api/v1/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(name=data['name'], age=data['age'], course=data['course'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201


@app.route('/api/v1/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{"id": student.id, "name": student.name, "age": student.age, "course": student.course} for student in students])

@app.route('/api/v1/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"id": student.id, "name": student.name, "age": student.age, "course": student.course})

@app.route('/api/v1/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.json
    student.name = data['name']
    student.age = data['age']
    student.course = data['course']
    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

@app.route('/api/v1/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200