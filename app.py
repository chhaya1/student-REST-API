# pylint: disable=R0903

"""
This module defines a simple Flask REST API for managing student records.
It uses SQLAlchemy for database operations and Flask-Migrate for handling migrations.
"""

import os
import socket

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
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

class Student(db.Model):
    """
    Student model represents a student record in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

@app.route("/", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    """
    hostname = socket.gethostname()
    return jsonify({"message": "Student API is up and running!", "hostname": hostname})

@app.route("/students", methods=["GET"])
def get_students():
    """
    Get all students.
    """
    students = Student.query.all()
    student_list = [{"id": student.id, "name": student.name, "age": student.age} for student in students]
    return jsonify(student_list)

@app.route("/students", methods=["POST"])
def create_student():
    """
    Create a new student record.
    """
    data = request.get_json()
    new_student = Student(name=data["name"], age=data["age"])
    db.session.add(new_student)  # pylint: disable=E1101
    db.session.commit()          # pylint: disable=E1101
    return jsonify({"message": "Student created"}), 201

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """
    Get a student by ID.
    """
    student = Student.query.get_or_404(student_id)
    return jsonify({"id": student.id, "name": student.name, "age": student.age})

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Update a student's information.
    """
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    student.name = data.get("name", student.name)
    student.age = data.get("age", student.age)
    db.session.commit()  # pylint: disable=E1101
    return jsonify({"message": "Student updated"})

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Delete a student record.
    """
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)  # pylint: disable=E1101
    db.session.commit()         # pylint: disable=E1101
    return jsonify({"message": "Student deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
