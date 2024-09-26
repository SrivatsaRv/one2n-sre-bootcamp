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

# Build the Docker image with semver tagging
build:
	@echo "Building Docker image with tag $(TAG)"
	@docker build -t $(IMAGE_NAME):$(TAG) .

# Run the MySQL container with volume persistence
run_db:
	@echo "Starting MySQL container with volume"
	@docker run --name $(SQL_CONTAINER_NAME) \
	    -v $(DB_VOLUME):/var/lib/mysql \
	    -e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
	    -e MYSQL_DATABASE=$(MYSQL_DATABASE) \
	    -e MYSQL_USER=$(MYSQL_USER) \
	    -e MYSQL_PASSWORD=$(MYSQL_PASSWORD) \
	    -d $(SQL_IMAGE)

wait_for_db:
	@echo "Waiting for MySQL to be ready..."
	@until docker exec -i mysql_container mysql -u$(MYSQL_USER) -p$(MYSQL_PASSWORD) -e "SHOW DATABASES;" > /dev/null 2>&1; do \
		echo "Waiting for MySQL..."; \
		sleep 5; \
	done


# Run the Flask container
run_flask:
	@echo "Starting Flask container"
	@docker run --name flask-app \
	    --env-file .env \
	    -p 5000:5000 \
	    --link $(SQL_CONTAINER_NAME):mysql \
	    -d $(IMAGE_NAME):$(TAG)

# Access the Flask container for Alembic migrations
access_flask:
	@docker exec -it flask-app /bin/bash

# Cleanup any existing containers
clean:
	@echo "Stopping and removing containers if they exist..."
	@docker stop flask-app $(SQL_CONTAINER_NAME) || true
	@docker rm flask-app $(SQL_CONTAINER_NAME) || true

# Migration steps
init_migrations:
	@echo "Initializing Alembic migrations"
	@docker exec -it flask-app bash -c "python3 -m flask db init"

generate_migration:
	@echo "Generating migration for the current schema"
	@docker exec -it flask-app bash -c 'python3 -m flask db migrate -m "dropped grade column"'

apply_migration_upgrade:
	@echo "Applying migration - type - upgrade"
	@docker exec -it flask-app bash -c "python3 -m flask db upgrade"

apply_migration_downgrade:
	@echo "Applying migration - type - downgrade"
	@docker exec -it flask-app bash -c "python3 -m flask db downgrade"

# Verify MySQL tables
verify_db:
	@docker exec -it $(SQL_CONTAINER_NAME) mysql -u $(MYSQL_USER) -p$(MYSQL_PASSWORD) -e "USE $(MYSQL_DATABASE); SHOW TABLES;"

# Full setup: Build, run DB, and Flask
all: build run_db wait_for_db run_flask init_migrations generate_migration apply_migration_upgrade