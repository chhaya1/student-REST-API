# Student API

A student CRUD REST API using Python and Flask.

## Functional Requirements

This API provides the following operations:

1. Add a new student.
2. Get all students.
3. Get a student by ID.
4. Update existing student information.
5. Delete a student record.

## Pre-requisites

Ensure the following tools are installed on your system:

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/
- Make: https://www.gnu.org/software/make/

## Setup Instructions

### 1. Build and Run the API

1. **Clone the repository:**
    ```bash
    git clone git@github.com:chhaya1/student-REST-API.git
    cd student-REST-API
    ```

2. **Create your `.env` file:**
    Add configurations such as database credentials:
    ```bash
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=
    DATABASE_URL=
    ```

3. **Build and run the application using Docker Compose:**
    ```bash
    make run
    ```

    This command will:
    - Start the PostgreSQL database container.
    - Initialize migrations.
    - Apply migrations to the database.
    - Build and run the REST API container.

4. **Access the API:**
    The API will be available at `http://localhost:5000`.

    Use an API client (e.g., Postman or curl) to interact with the API endpoints.

### 2. Manage Database Migrations

The following `Makefile` targets will help with database migrations:

- **Initialize migrations folder:**
    ```bash
    make init-migrations
    ```

- **Generate migration script each time the model is updated:**
    ```bash
    make migrate-db
    ```

- **Apply migrations to the database:**
    ```bash
    make upgrade-db
    ```

### 3. Running the API and Database

- To **start the database** without starting the API:
    ```bash
    make start-db
    ```

- To **build and run the API** without running the database:
    ```bash
    make build-api
    make run-api
    ```

## API Endpoints

The following endpoints are available in the API:

1. **Healthcheck**
   - `GET /api/v1/healthcheck`
   - Example response: `{"status": "healthy"}`

2. **Get all students**
   - `GET /api/v1/students`
   - Example response:
     ```json
     [
       {"id": 1, "name": "Chhaya", "age": 21, "major": "Computer Science"},
       {"id": 2, "name": "Harshita", "age": 22, "major": "Mathematics"}
     ]
     ```

3. **Get a student by ID**
   - `GET /api/v1/students/{id}`
   - Example response:
     ```json
     {"id": 1, "name": "Chhaya", "age": 21, "major": "Computer Science"}
     ```

4. **Add a new student**
   - `POST /api/v1/students`
   - Example request:
     ```json
     {"name": "Chhaya", "age": 21, "major": "Computer Science"}
     ```
   - Example response:
     ```json
     {"id": 1, "name": "Chhaya", "age": 21, "major": "Computer Science"}
     ```

5. **Update a student**
   - `PUT /api/v1/students/{id}`
   - Example request:
     ```json
     {"name": "Harshita", "age": 25, "major": "Mathematics"}
     ```
   - Example response:
     ```json
     {"id": 1, "name": "Harshita", "age": 25, "major": "Mathematics"}
     ```

6. **Delete a student**
   - `DELETE /api/v1/students/{id}`
   - Example response:
     ```json
     {"message": "Student deleted successfully"}
     ```