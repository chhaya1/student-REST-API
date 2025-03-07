import unittest
import os
from app import app, db, Student
from dotenv import load_dotenv

class TestStudentAPI(unittest.TestCase):

    def setUp(self):
        """Set up the Flask test client and configure the test PostgreSQL database."""
        load_dotenv()  # Load environment variables from .env file

        # Use TEST_DATABASE_URL for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()

        with app.app_context():
            db.create_all()  # Create tables for the test

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()  # Remove session
            db.drop_all()  # Drop tables after test

    def test_healthcheck(self):
        """Test the healthcheck endpoint."""
        response = self.app.get('/api/v1/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_get_students(self):
        """Test getting the list of students."""
        # Add a student to the database for testing
        student = Student(name="John Doe", age=20, major="Computer Science")
        db.session.add(student)
        db.session.commit()

        response = self.app.get('/api/v1/students')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)  # Check if there are students in the response

    def test_get_student(self):
        """Test getting a single student by ID."""
        # Add a student to the database for testing
        student = Student(name="Jane Doe", age=22, major="Mathematics")
        db.session.add(student)
        db.session.commit()

        response = self.app.get(f'/api/v1/students/{student.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Jane Doe')

    def test_add_student(self):
        """Test adding a new student."""
        new_student = {
            "name": "Alice Smith",
            "age": 21,
            "major": "Physics"
        }

        response = self.app.post('/api/v1/students', json=new_student)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Alice Smith')

    def test_update_student(self):
        """Test updating an existing student."""
        # Add a student to the database for testing
        student = Student(name="Bob Johnson", age=23, major="Chemistry")
        db.session.add(student)
        db.session.commit()

        updated_data = {
            "name": "Robert Johnson",
            "age": 24,
            "major": "Biology"
        }

        response = self.app.put(f'/api/v1/students/{student.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Robert Johnson')
        self.assertEqual(response.json['age'], 24)
        self.assertEqual(response.json['major'], 'Biology')

    def test_delete_student(self):
        """Test deleting a student."""
        # Add a student to the database for testing
        student = Student(name="Charlie Brown", age=25, major="Physics")
        db.session.add(student)
        db.session.commit()

        response = self.app.delete(f'/api/v1/students/{student.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Student deleted successfully')

        # Check if the student was really deleted
        deleted_student = Student.query.get(student.id)
        self.assertIsNone(deleted_student)

if __name__ == "__main__":
    unittest.main()
