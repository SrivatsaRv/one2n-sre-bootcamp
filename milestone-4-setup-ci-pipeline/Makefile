# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Variables for Docker operations
IMAGE_NAME = ${DOCKERHUB_USERNAME}/one2n-bootcamp
SQL_CONTAINER_NAME = mysql_container
SQL_IMAGE = mysql:8.0
DB_VOLUME = mysql_data
TAG ?= 1.4.0  # Default semantic version for the image, changeable via command line
NETWORK_NAME = flask_network
VENV_DIR = venv  # Virtual environment directory

# Define a default DB_HOST that can be overridden
DB_HOST ?= 127.0.0.1

# Ensure the .env file contains necessary variables..
check_env:
	@if [ ! -f ".env" ]; then \
		echo "Error: .env file not found."; \
		exit 1; \
	fi
	@echo "Using environment variables from .env file"

# Virtual environment setup for local development....
venv_setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Activating virtual environment and installing dependencies..."
	. venv/bin/activate && pip install -r requirements.txt

# Start the MySQL container using Docker Compose
run_db:
	@echo "Starting MySQL container using Docker Compose"
	@docker compose up -d mysql && sleep 10

# Initialize Alembic migrations locally (First-time setup)
init_migrations:
	@if [ -d "migrations" ]; then \
		echo "Migrations folder exists, skipping init."; \
	else \
		echo "Initializing Alembic migrations"; \
		flask db init; \
	fi

# Generate a new migration based on models.py changes (ensure it's executed)
generate_migration:
	@echo "Generating migration (if necessary)..."
	@DB_URL=mysql://root:${MYSQL_ROOT_PASSWORD}@127.0.0.1:3306/${MYSQL_DATABASE} flask db migrate -m "Auto-generated migration"
	
# Lint the code using flake8
lint:
	@echo "Running code linting with flake8..."
	/Users/admin/one2n-sre-bootcamp/milestone-4-setup-ci-pipeline/venv/bin/flake8 app.py tests/test_app.py models.py

# Run tests using pytest
run_tests:
	@echo "Running tests using test_student_db..."
	@PYTHONPATH=./ FLASK_ENV=testing DB_URL=mysql://root:${MYSQL_ROOT_PASSWORD}@127.0.0.1:3306/test_student_db python3 -m pytest tests/test_app.py

# Build Flask API Docker image with version tag
build_flask_image:
	@echo "Building Flask API Docker image with version $(TAG)..."
	@docker build -t $(IMAGE_NAME):$(TAG) .


# Login to DockerHub using Personal Access Token (non-interactive)..
docker_login:
	@echo "Logging in to DockerHub..."
	@echo "${DOCKERHUB_TOKEN}" | docker login --username "${DOCKERHUB_USERNAME}" --password-stdin

# Push Docker image to DockerHub
docker_push:
	@echo "Pushing Docker image to DockerHub..."
	@docker push $(IMAGE_NAME):$(TAG)

# Full pipeline including Docker login and push
deploy_pipeline: ci_pipeline docker_login docker_push

# Clean up any existing containers and network
clean:
	@echo "Cleaning up all app-related Docker containers, networks, images, and volumes..."
	# Stop and remove containers associated with flask_api and the MySQL container
	@docker compose down --rmi all --volumes

# Full CI pipeline: DB Up -> Migrations -> Generate Migration -> Build API -> Run Tests -> Lint -> Everything Works -> Login and Push to Docker 
ci_pipeline: check_env run_db init_migrations generate_migration lint run_tests build_flask_image docker_login docker_push

## OPTIONAL - FOR MILESTONE-4
# Start the Flask API container using Docker Compose and set the image version

run_flask_container:
	@echo "Starting Flask API container with version $(TAG)"
	@API_VERSION=$(TAG) DB_URL=mysql://root:${MYSQL_ROOT_PASSWORD}@mysql_container:3306/${MYSQL_DATABASE} docker compose up -d api