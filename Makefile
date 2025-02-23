# Local setup:

# Install dependencies
install:
	pip install -r requirements.txt

# Run the Flask app locally
run-local:
	python3 app.py

# Docker setup:docker

# Build Docker image
build:
	docker build -t student-api:1.0.0 .

# Run the app as Docker container
run-docker:
	docker run -p 5001:5000 -e DATABASE_URL=postgresql://postgres:postgres@localhost:5432/students student-api:1.0.0
