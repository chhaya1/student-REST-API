DOCKER_IMAGE=chhaya786/student-api
VERSION=1.0.1

# Target to start the DB container
start-db:
	docker-compose up -d db

# Target to initialize the migrations folder
init-migrations:
	docker-compose run api flask db init

# Target to generate a new migration (detect changes in models)
migrate-db:
	docker-compose run api flask db migrate

# Target to apply migrations to the DB (run 'flask db upgrade')
upgrade-db:
	docker-compose run api flask db upgrade

# Target to build the REST API docker image
build-api:
	docker-compose build api

# Target to run the REST API docker container
run-api:
	docker-compose up api

# All-in-one target (DB start, migrations, API start)
run:
	make start-db
	sleep 10  # Ensure the DB has started
	make init-migrations
	make migrate-db
	make upgrade-db
	make run-api

# Target to run the tests
test:
	python -m unittest discover

# Target to perform linting
lint:
	pylint app.py

# Target to build and push Docker image with version to the Dockerhub
docker-push:
	docker build -t $(DOCKER_IMAGE):$(VERSION) .
	docker push $(DOCKER_IMAGE):$(VERSION)

