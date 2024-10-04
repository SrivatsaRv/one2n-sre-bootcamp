# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Variables for Docker operations
IMAGE_NAME = flask-api
SQL_CONTAINER_NAME = mysql_container
SQL_IMAGE = mysql:8.0
DB_VOLUME = mysql_data
TAG ?= 1.0.0  # Default semantic version for the image, changeable via command line
NETWORK_NAME = flask_network
VENV_DIR = venv  # Virtual environment directory

# Define a default DB_HOST that can be overridden
DB_HOST ?= 127.0.0.1

# Ensure the .env file contains necessary variables
check_env:
	@if [ ! -f ".env" ]; then \
		echo "Error: .env file not found."; \
		exit 1; \
	fi
	@echo "Using environment variables from .env file"

# Virtual environment setup for local development
venv_setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Activating virtual environment and installing dependencies..."
	. venv/bin/activate && pip install -r requirements.txt

# Start the MySQL container using Docker Compose
run_db:
	@echo "Starting MySQL container using Docker Compose"
	@docker-compose up -d mysql && sleep 10

# Initialize Alembic migrations locally (First-time setup)
init_migrations:
	@echo "Initializing Alembic migrations..."
	@flask db init

# Generate a new migration based on models.py changes
generate_migration:
	@echo "Generating migration..."
	@DB_URL=mysql://root:${MYSQL_ROOT_PASSWORD}@$(DB_HOST):3306/${MYSQL_DATABASE} flask db migrate -m "Auto-generated migration"

# Build Flask API image with version tag
build_api:
	@echo "Building Flask API image with version $(TAG)..."
	@docker build -t $(IMAGE_NAME):$(TAG) .

# Start the Flask API container using Docker Compose and set the image version
run_api:
	@echo "Starting Flask API container with version $(TAG)"
	@API_VERSION=$(TAG) DB_URL=mysql://root:${MYSQL_ROOT_PASSWORD}@mysql_container:3306/${MYSQL_DATABASE} docker-compose up -d api

# Run tests using pytest with the test_student_db
run_tests:
	@echo "Running tests using test_student_db..."
	@PYTHONPATH=./ FLASK_ENV=testing DB_URL=mysql://root:${MYSQL_ROOT_PASSWORD}@$(DB_HOST):3306/test_student_db pytest tests/test_app.py


lint:
	flake8 app.py tests/test_app.py models.py
# Full setup: DB Up -> Init Migrations -> Generate Migration -> Build Image -> Run Container -> Container Handles Migrations -> Run Tests

all: run_db build_api run_api run_tests lint
#all: run_db init_migrations generate_migration build_api run_api run_tests


# Clean up any existing containers and network
clean:
	@echo "Stopping and removing containers if they exist..."  
	@docker stop flask_api $(SQL_CONTAINER_NAME)
	@docker rm flask_api $(SQL_CONTAINER_NAME)
	@docker network rm $(NETWORK_NAME)


# Full CI pipeline: Run DB -> Init Migrations -> Generate Migration -> Build API -> Run Tests
ci_pipeline: check_env run_db init_migrations generate_migration build_api run_api run_tests