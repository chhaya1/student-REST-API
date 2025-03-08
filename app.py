# pylint: disable=R0903

"""
This module defines a simple Flask REST API for managing student records.
It uses SQLAlchemy for database operations and Flask-Migrate for handling migrations.
"""

import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app (app).
app = Flask(__name__)

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure the DATABASE_URL is set correctly
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Configure SQLAlchemy with the database URL
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Student model
class Student(db.Model):
    """
    Student model representing a student record in the database.
    """
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=no-member
    name = db.Column(db.String(50), nullable=False)  # pylint: disable=no-member
    age = db.Column(db.Integer, nullable=False)  # pylint: disable=no-member
    major = db.Column(db.String(50), nullable=True)  # pylint: disable=no-member

# Healthcheck endpoint
@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    """
    Healthcheck endpoint to verify if the API is running.
    """
    return jsonify({"status": "healthy"}), 200

# Get all students
@app.route('/api/v1/students', methods=['GET'])
def get_students():
    """
    Get a list of all students.
    """
    students = Student.query.all()
    return jsonify([{
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "major": student.major
    } for student in students]), 200

# Get a student by ID
@app.route('/api/v1/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """
    Get a student by their ID.
    """
    student = Student.query.get_or_404(student_id)
    return jsonify({
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "major": student.major
    }), 200

# Add a new student
@app.route('/api/v1/students', methods=['POST'])
def add_student():
    """
    Add a new student to the database.
    """
    new_student = request.get_json()
    student = Student(
        name=new_student["name"],
        age=new_student["age"],
        major=new_student.get("major")
    )
    db.session.add(student)  # pylint: disable=no-member
    db.session.commit()  # pylint: disable=no-member
    return jsonify({
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "major": student.major
    }), 201

# Update an existing student
@app.route('/api/v1/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """
    Update an existing student's details.
    """
    student = Student.query.get_or_404(student_id)
    updated_data = request.get_json()
    student.name = updated_data.get("name", student.name)
    student.age = updated_data.get("age", student.age)
    student.major = updated_data.get("major", student.major)
    db.session.commit()  # pylint: disable=no-member
    return jsonify({
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "major": student.major
    }), 200

# Delete a student
@app.route('/api/v1/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    Delete a student from the database.
    """
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)  # pylint: disable=no-member
    db.session.commit()  # pylint: disable=no-member
    return jsonify({"message": "Student deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
