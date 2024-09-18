from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    grade = data.get('grade')

    conn = get_db_connection()
    conn.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student added successfully'}), 201

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()

    return jsonify([dict(student) for student in students]), 200

# Get a student by ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()

    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify(dict(student)), 200

# Update student information
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    grade = data.get('grade')

    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    conn.execute('UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?', (name, age, grade, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student updated successfully'}), 200

# Delete a student record
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Student with ID {id} has been deleted.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
