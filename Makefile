# Install dependencies locally
install:
	pip install -r requirements.txt

# Run the Flask app locally
run-local:
	python3 app.py

# Docker setup

# Build Docker image
build:
	docker build -t student-api:1.0.1 .
start:
	docker-compose up -d db  # Start DB container
	flask db migrate -m "Initial migration"  # Run migration
	flask db upgrade         # Apply migrations
	docker-compose up -d api # Start API container