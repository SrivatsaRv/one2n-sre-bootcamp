# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

DB_URL = $(DATABASE_URL)  # Load DATABASE_URL from .env
TEST_DB_URL_ENV = $(TEST_DB_URL)  # Load TEST_DB_URL from .env

# Setup virtual environment only if it doesn't already exist
setup_venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Setting up virtual environment"; \
		python3 -m venv $(VENV_DIR); \
	fi

# Install dependencies inside the virtual environment
install_dependencies: setup_venv
	@echo "Installing dependencies"
	@$(PIP) install -r requirements.txt

# Check if MySQL is installed
check_mysql:
	@if ! command -v mysql &> /dev/null; then \
		echo "Error: MySQL is not installed. Please install MySQL and try again."; \
		exit 1; \
	fi

# Create MySQL production and test databases if they don't exist
create_db: check_mysql
	@echo "Creating MySQL production and test databases"
	@mysql -u $(MYSQL_ROOT_USER) -e "CREATE DATABASE IF NOT EXISTS $(MYSQL_DATABASE);"
	@mysql -u $(MYSQL_ROOT_USER) -e "CREATE DATABASE IF NOT EXISTS test_student_db;"
	@mysql -u $(MYSQL_ROOT_USER) -e "CREATE USER IF NOT EXISTS '$(MYSQL_USER)'@'localhost' IDENTIFIED BY '$(MYSQL_PASSWORD)';"
	@mysql -u $(MYSQL_ROOT_USER) -e "GRANT ALL PRIVILEGES ON $(MYSQL_DATABASE).* TO '$(MYSQL_USER)'@'localhost';"
	@mysql -u $(MYSQL_ROOT_USER) -e "GRANT ALL PRIVILEGES ON test_student_db.* TO '$(MYSQL_USER)'@'localhost';"
	@mysql -u $(MYSQL_ROOT_USER) -e "FLUSH PRIVILEGES;"

# Reset the Alembic version table in MySQL (if it exists)
reset_alembic_version: check_mysql
	@echo "Resetting Alembic version in the production database"
	@mysql -u $(MYSQL_ROOT_USER) -e "USE $(MYSQL_DATABASE); DROP TABLE IF EXISTS alembic_version;"

# Initialize Alembic (if not already done)
init_migrations: check_mysql
	@if [ ! -d "migrations" ]; then \
		echo "Initializing Alembic migrations"; \
		FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db init; \
		echo "Generating and applying initial migration for student table"; \
		FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db migrate -m "Initial commit: Create student table"; \
		FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db upgrade; \
	fi

# Generate migration based on models.py schema (tracks changes in schema)
generate_migration: check_mysql
	@echo "Generating Alembic migration"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db migrate -m "Schema changes"

# Apply database migrations (runs upgrade)
apply_migration: check_mysql
	@echo "Applying database migrations"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db upgrade



# Start Flask application
start_app: install_dependencies create_db reset_alembic_version init_migrations generate_migration apply_migration
	@echo "Starting Flask Application"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) app.py

# Resume Flask application without setup (useful for restarting the server after it has already been set up)
resume_flask:
	@echo "Resuming Flask Application"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) app.py

# Create MySQL test database if it doesn't exist
create_test_db: check_mysql
	@echo "Creating MySQL test database"
	@mysql -u $(MYSQL_ROOT_USER) -e "CREATE DATABASE IF NOT EXISTS test_student_db;"

# Run tests using pytest and ensure test database exists
run_tests: create_test_db
	@echo "Running tests"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(TEST_DB_URL_ENV) $(PYTHON) -m pytest --disable-warnings

# The 'all' target that runs everything in order
all: install_dependencies check_mysql create_db reset_alembic_version init_migrations generate_migration apply_migration start_app

# Cleanup target to remove virtual environment and generated files (but not migrations)
clean:
	rm -rf $(VENV_DIR) __pycache__/ .pytest_cache__/ *.db *.log

# Full clean, including migrations (use with caution)
full_clean: clean
	rm -rf migrations/