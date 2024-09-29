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
	@docker-compose up -d mysql

# Initialize Alembic migrations locally (First-time setup) - RUNS LOCALLY
init_migrations:
	@echo "Initializing Alembic migrations locally"
	@flask db init

# Generate a new migration based on models.py changes locally - RUNS LOCALLY
generate_migration:
	@echo "Generating latest migration based on model changes"
	@flask db migrate -m "Generate migration"

# Build Flask API image with version tag
build_api:
	@echo "Building Flask API image with version $(TAG)"
	@docker build -t $(IMAGE_NAME):$(TAG) .

# Start the Flask API container using Docker Compose and set the image version
run_api:
	@echo "Starting Flask API container with version $(TAG)"
	@API_VERSION=$(TAG) docker-compose up -d api

# Clean up any existing containers and network
clean:
	@echo "Stopping and removing containers if they exist..."
	@docker stop flask-app $(SQL_CONTAINER_NAME) || true
	@docker rm flask-app $(SQL_CONTAINER_NAME) || true
	@docker network rm $(NETWORK_NAME) || true

# Full setup: Build Flask API image, run DB, initialize migrations, run Flask, apply migrations
all: build_api run_db init_migrations generate_migration run_api