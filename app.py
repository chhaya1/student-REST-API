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

# Define the Student model
class Student(db.Model):
    """Model representing a student."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Define routes
@app.route("/students", methods=["GET"])
def get_students():
    """Fetch all students from the database."""
    students = Student.query.all()
    return jsonify([{"id": student.id, "name": student.name, "age": student.age} for student in students])

@app.route("/students", methods=["POST"])
def create_student():
    """Create a new student record."""
    data = request.get_json()
    new_student = Student(name=data['name'], age=data['age'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student created successfully"}), 201

@app.route("/health", methods=["GET"])
def health_check():
    """Check the health of the application."""
    return jsonify({
        "status": "OK",
        "hostname": socket.gethostname()
    })

# Run the app (optional, usually not needed if using gunicorn/uwsgi)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
