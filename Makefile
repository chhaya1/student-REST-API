DOCKER_IMAGE=chhaya786/student-api
VERSION=1.0.2

# Target to start the DB container
start-db:
	docker-compose up -d db

# Target to initialize the migrations folder (only once)
init-migrations:
	docker-compose run api1 flask db init

# Target to generate a new migration (detect changes in models)
migrate-db:
	docker-compose run api1 flask db migrate

# Target to apply migrations to the DB
upgrade-db:
	docker-compose run api1 flask db upgrade

# Target to build the REST API docker images
build-api:
	docker-compose build api1 api2

# Target to run the REST API containers
run-api:
	docker-compose up -d api1 api2
run-nginx:
	docker-compose up -d nginx

# All-in-one target (DB start, migrations, API start)
run:
	make start-db
	sleep 10  # Ensure the DB has started
	make init-migrations       # Initialize migrations only once for both API containers
	make migrate-db            # Generate migrations for the shared migrations folder
	make upgrade-db            # Apply migrations to the DB
	make run-api               # Start both API containers
	make run-nginx

# Target to run the tests
test:
	python -m unittest discover

# Target to perform linting
lint:
	pylint app.py

# Target to build and push Docker image with version to Dockerhub
docker-push:
	docker build -t $(DOCKER_IMAGE):$(VERSION) .
	docker push $(DOCKER_IMAGE):$(VERSION)