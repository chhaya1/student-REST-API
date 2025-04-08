# pylint: disable=R0903

"""
This module defines a simple Flask REST API for managing student records.
It uses SQLAlchemy for database operations and Flask-Migrate for handling migrations.
"""

import os
import socket

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String  # <-- FIXED import
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
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)

@app.route("/", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    """
    hostname = socket.gethostname()
    return jsonify({"message": f"Hello from {hostname}!"})

@app.route("/students", methods=["POST"])
def add_student():
    """
    Endpoint to add a new student.
    """
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")

    if not name or age is None:
        return jsonify({"error": "Name and age are required"}), 400

    new_student = Student(name=name, age=age)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message": "Student added successfully"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
