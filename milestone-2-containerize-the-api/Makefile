# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Variables for Docker operations
IMAGE_NAME = flask-app
SQL_CONTAINER_NAME = mysql_container
SQL_IMAGE = mysql:8.0
DB_VOLUME = mysql_data
TAG = 1.0.0
NETWORK_NAME = flask_network
VENV_DIR = venv  # Virtual environment directory

# Virtual environment setup
venv_setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Activating virtual environment and installing dependencies..."
	. venv/bin/activate && pip install -r requirements.txt

# Run the MySQL container with volume persistence and expose it to localhost
run_db: create_network
	@echo "Starting MySQL container with volume"
	@docker run --name $(SQL_CONTAINER_NAME) --network $(NETWORK_NAME) \
	    -v $(DB_VOLUME):/var/lib/mysql \
	    -e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
	    -e MYSQL_DATABASE=$(MYSQL_DATABASE) \
	    -e MYSQL_USER=$(MYSQL_USER) \
	    -e MYSQL_PASSWORD=$(MYSQL_PASSWORD) \
	    -p 3306:3306 \
	    -d $(SQL_IMAGE)

# Create a custom Docker network for communication between containers
create_network:
	@echo "Creating Docker network"
	@docker network create $(NETWORK_NAME) || true

# Wait for MySQL to be ready
wait_for_db:
	@echo "Waiting for MySQL to be ready..."
	@until docker exec -i $(SQL_CONTAINER_NAME) mysql -u$(MYSQL_USER) -p$(MYSQL_PASSWORD) -e "SHOW DATABASES;" > /dev/null 2>&1; do \
		echo "Waiting for MySQL..."; \
		sleep 5; \
	done

# Source .env and initialize Alembic migrations locally (First-time setup) - RUNS LOCALLY
init_migrations:
	@echo "Sourcing .env and initializing Alembic migrations locally"
	@source .env && python3 -m flask db init

# Source .env and generate a new migration based on models.py changes locally - RUNS LOCALLY
generate_migration:
	@echo "Flask-Alembic is Generating Latest Migration File - Please Wait ....Underway"
	@source .env && python3 -m flask db migrate -m "Create tables"

# Source .env and apply migration to the running MySQL container - RUNS INSIDE APP CONTAINER
apply_migration_upgrade:
	@echo "Flask Apply Underway - Please wait - Container Applying Changes - Type - Upgrade"
	@python3 -m flask db upgrade

# Downgrade migration (optional)
apply_migration_downgrade:
	@echo "Flask Apply Underway - Please wait - Container Applying Changes - Type - Downgrade"
	@python3 -m flask db downgrade

# Verify MySQL tables and prints schema
verify_db:
	@echo "Verifying MySQL schema"
	@docker exec -it $(SQL_CONTAINER_NAME) mysql -u $(MYSQL_USER) -p$(MYSQL_PASSWORD) -e "USE $(MYSQL_DATABASE); DESCRIBE student;"


# Build the Docker image with semver tagging
build:
	@echo "Building Docker image with tag $(TAG)"
	@docker build -t $(IMAGE_NAME):$(TAG) .

# Run the Flask container
run_flask:
	@echo "Starting Flask container"
	@docker run --name flask-app --network $(NETWORK_NAME) \
	    --env-file .env \
	    -p 5000:5000 \
	    -d $(IMAGE_NAME):$(TAG)

		
# Clean up any existing containers
clean:
	@echo "Stopping and removing containers if they exist..."
	@docker stop flask-app $(SQL_CONTAINER_NAME) || true
	@docker rm flask-app $(SQL_CONTAINER_NAME) || true
	@docker network rm $(NETWORK_NAME) || true

# Full setup: Build, run DB, wait for DB, run Flask
all: build run_db wait_for_db run_flask verify_db