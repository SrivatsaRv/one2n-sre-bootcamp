# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
DB_URL = mysql://$(MYSQL_USER):$(MYSQL_PASSWORD)@localhost/$(MYSQL_DATABASE)
MYSQL_ROOT_USER = root
MYSQL_ROOT_PASSWORD = ''  # Set your MySQL root password here if necessary
MYSQL_DATABASE = $(shell grep DB_NAME .env | cut -d '=' -f2)
MYSQL_USER = $(shell grep DB_USER .env | cut -d '=' -f2)
MYSQL_PASSWORD = $(shell grep DB_PASSWORD .env | cut -d '=' -f2)

# Function to generate random password
RANDOM_PASSWORD := $(shell openssl rand -hex 12)

# Setup virtual environment only if it doesn't already exist
setup_venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Setting up virtual environment"; \
		python3 -m venv $(VENV_DIR); \
	fi

# Check if the .env file exists, create if not, and generate random password
check_env:
	@if [ ! -f .env ]; then \
		echo "No .env file found. Creating one..."; \
		touch .env; \
		echo "DB_USER=youruser" > .env; \
		echo "DB_PASSWORD=$(RANDOM_PASSWORD)" >> .env; \
		echo "DB_HOST=localhost" >> .env; \
		echo "DB_NAME=student_db" >> .env; \
		echo ".env file created with random password."; \
	fi

# Install dependencies inside the virtual environment
install_dependencies: setup_venv
	@echo "Installing dependencies"
	@$(PIP) install -r requirements.txt

# Create MySQL database if it doesn't exist and create user
create_db: check_env
	@echo "Creating MySQL database and user"
	@mysql -u $(MYSQL_ROOT_USER) --password=$(MYSQL_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS $(MYSQL_DATABASE);"
	@mysql -u $(MYSQL_ROOT_USER) --password=$(MYSQL_ROOT_PASSWORD) -e "CREATE USER IF NOT EXISTS '$(MYSQL_USER)'@'localhost' IDENTIFIED BY '$(MYSQL_PASSWORD)';"
	@mysql -u $(MYSQL_ROOT_USER) --password=$(MYSQL_ROOT_PASSWORD) -e "GRANT ALL PRIVILEGES ON $(MYSQL_DATABASE).* TO '$(MYSQL_USER)'@'localhost';"
	@mysql -u $(MYSQL_ROOT_USER) --password=$(MYSQL_ROOT_PASSWORD) -e "FLUSH PRIVILEGES;"

# Reset the Alembic version table in MySQL (if it exists)
reset_alembic_version: check_env
	@echo "Resetting Alembic version in the database"
	@mysql -u $(MYSQL_ROOT_USER) --password=$(MYSQL_ROOT_PASSWORD) -e "USE $(MYSQL_DATABASE); DROP TABLE IF EXISTS alembic_version;"

# Initialize Alembic (if not already done)
init_migrations: check_env
	@if [ ! -d "migrations" ]; then \
		echo "Initializing Alembic migrations"; \
		FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db init; \
	fi

# Generate migration based on models.py schema (tracks changes in schema)
generate_migration: check_env
	@echo "Generating Alembic migration"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db migrate -m "Initial migration"

# Apply database migrations (runs upgrade)
apply_migration: check_env
	@echo "Applying database migrations"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db upgrade

# Start Flask application
start_app: install_dependencies create_db reset_alembic_version init_migrations generate_migration apply_migration
	@echo "Starting Flask Application"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) app.py

# The 'all' target that runs everything in order
all: install_dependencies create_db reset_alembic_version init_migrations generate_migration apply_migration start_app

# Run tests using pytest
run_tests:
	@echo "Running tests"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m pytest --disable-warnings

# Cleanup target to remove virtual environment and generated files (but not migrations)
clean:
	rm -rf $(VENV_DIR) __pycache__/ .pytest_cache/ *.db *.log

# Full clean, including migrations (use with caution)
full_clean: clean
	rm -rf migrations/ instance/