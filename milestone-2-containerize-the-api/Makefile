# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Variables for Docker operations
IMAGE_NAME = flask-app
SQL_CONTAINER_NAME = mysql_container   # This is the name of the container
SQL_IMAGE = mysql:8.0                  # This is the image to use for MySQL
DB_VOLUME = mysql_data
TAG = 1.0.0

# Build the Docker image with semver tagging
build:
	@echo "Building Docker image with tag $(TAG)"
	@docker build -t $(IMAGE_NAME):$(TAG) .

# Run the MySQL container with volume persistence
run_db:
	@echo "Starting MySQL container with volume"
	@docker volume create $(DB_VOLUME)
	@docker run --name $(SQL_CONTAINER_NAME) -v $(DB_VOLUME):/var/lib/mysql \
	    -e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
	    -e MYSQL_DATABASE=$(MYSQL_DATABASE) \
	    -e MYSQL_USER=$(MYSQL_USER) \
	    -e MYSQL_PASSWORD=$(MYSQL_PASSWORD) \
	    -d $(SQL_IMAGE)

# Wait for the MySQL container to be ready
wait_for_db:
	@echo "Waiting for MySQL to be ready..."
	@until docker exec -i $(SQL_CONTAINER_NAME) mysql -u$(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "SHOW DATABASES;" > /dev/null 2>&1; do \
	    echo "Waiting for database connection..."; \
	    sleep 3; \
	done

# Start the Flask app container only if it's not already running
start_flask_if_needed:
	@if ! docker ps -q --filter "name=flask-app"; then \
		echo "Starting Flask container"; \
		docker run -d --name flask-app --env-file .env -p 5000:5000 $(IMAGE_NAME):$(TAG); \
		sleep 5; \
		if ! docker ps -q --filter "name=flask-app"; then \
			echo "Error: Flask container failed to start"; \
			docker logs flask-app; \
			exit 1; \
		fi; \
	else \
		echo "Flask container is already running"; \
	fi

# Initialize Alembic migrations (if not already done)
init_migrations:
	@echo "Initializing Alembic migrations (if not already done)"
	@if docker ps -q --filter "name=flask-app"; then \
		if ! docker exec flask-app test -d "migrations"; then \
			echo "Initializing Alembic migrations"; \
			docker exec flask-app bash -c "FLASK_APP=app.py python3 -m flask db init"; \
			echo "Generating and applying initial migration for student table"; \
			docker exec flask-app bash -c "FLASK_APP=app.py python3 -m flask db migrate -m 'Initial commit: Create student table'"; \
			docker exec flask-app bash -c "FLASK_APP=app.py python3 -m flask db upgrade"; \
		fi \
	else \
		echo "Error: flask-app container not running"; \
		exit 1; \
	fi

# Apply database migrations (runs upgrade)
apply_migration:
	@echo "Applying database migrations"
	@if docker ps -q --filter "name=flask-app"; then \
		docker exec flask-app bash -c "FLASK_APP=app.py python3 -m flask db upgrade"; \
	else \
		echo "Error: flask-app container not running"; \
		exit 1; \
	fi

# Clean up containers and volumes efficiently
clean:
	@echo "Stopping and removing containers if they exist..."
	@if docker ps -q --filter "name=flask-app"; then \
		docker stop flask-app && docker rm -f flask-app; \
	else \
		echo "flask-app container does not exist."; \
	fi
	@if docker ps -q --filter "name=$(SQL_CONTAINER_NAME)"; then \
		docker stop $(SQL_CONTAINER_NAME) && docker rm -f $(SQL_CONTAINER_NAME); \
	else \
		echo "$(SQL_CONTAINER_NAME) container does not exist."; \
	fi
	@echo "Removing Docker volume if it exists..."
	@if docker volume ls -q --filter "name=$(DB_VOLUME)"; then \
		docker volume rm -f $(DB_VOLUME); \
	else \
		echo "$(DB_VOLUME) volume does not exist."; \
	fi

# Full clean target (removes Docker containers and volumes)
full_clean: clean
	@echo "Removing all Docker images built by this project..."
	@if docker images -q $(IMAGE_NAME):$(TAG); then \
		docker rmi $(IMAGE_NAME):$(TAG); \
	else \
		echo "$(IMAGE_NAME) image does not exist."; \
	fi

# Default target that builds the image, runs the database, and applies schema
all: build run_db wait_for_db start_flask_if_needed init_migrations apply_migration
	@echo "All steps completed."