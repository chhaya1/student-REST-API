from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import psycopg2

#Load environment variables from .env file
load_dotenv()

#Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

#Initialize Flask app
app = Flask(__name__)

#Database connection using psycopg2
def get_db_connection():
    connection = psycopg2.connect(DATABASE_URL)
    return connection 

#Healthcheck endpoint
@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    conn = get_db_connection() 
    if conn:
        return jsonify({"status": "healthy", "db_url": DATABASE_URL}), 200
    return jsonify({"status": "error", "message": "Could not connect to the database"}), 500

#Get all students
@app.route('/api/v1/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students;") 
        students = cur.fetchall() 
        cur.close()
        return jsonify([{"id": student[0], "name": student[1], "age": student[2], "major": student[3]} for student in students]), 200
    return jsonify({"error": "Database connection failed"}), 500

#Get a student by ID
@app.route('/api/v1/students/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = %s;", (id,))
        student = cur.fetchone()
        cur.close() 
        if student: 
            return jsonify({"id": student[0], "name": student[1], "age": student[2], "major": student[3]}), 200
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"error": "Database connection failed"}), 500

#Add a new student
@app.route('/api/v1/students', methods=['POST'])
def add_student():
    new_student = request.get_json()
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, age) VALUES (%s, %s) RETURNING id;", 
                    (new_student["name"], new_student["age"]))
        student_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({"id": student_id, "name": new_student["name"], "age": new_student["age"]}), 201
    return jsonify

#Update student information
@app.route('/api/v1/students/<int:id>', methods=['PUT'])
def update_student(id):
    updated_info = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE students SET name = %s, age = %s WHERE id = %s', 
                (updated_info["name"], updated_info["age"], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Student updated successfully"}), 200

#Delete a student record
@app.route('/api/v1/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM students WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Student deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
