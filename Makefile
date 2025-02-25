# Local setup:

# Install dependencies
install:
	pip install -r requirements.txt

# Run the Flask app locally
run-local:
	python3 app.py

# Docker setup

# Build Docker image
build:
	docker build -t student-api:1.0.1 .

# Run db container
start-db:
	docker-compose up -d db

# Run the app as Docker container
run-docker:
	docker-compose up api
