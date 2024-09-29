# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Variables
VENV_DIR = venv
ACTIVATE = source $(VENV_DIR)/bin/activate
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

DB_URL = $(DATABASE_URL)  # Load DATABASE_URL from .env
TEST_DB_URL_ENV = $(TEST_DB_URL)  # Load TEST_DB_URL from .env

# Install dependencies inside the virtual environment
install_dependencies:
	@echo "Installing dependencies" 
	@$(PIP) install -r requirements.txt

# Setup virtual environment only if it doesn't already exist
setup_venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Setting up virtual environment"; \
		python3 -m venv $(VENV_DIR); \
	fi

# Create MySQL production and test databases if they don't exist
create_db:
	@echo "Creating MySQL production and test databases"
	-@mysql -u $(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS $(MYSQL_DATABASE);"
	-@mysql -u $(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS test_student_db;"
	-@mysql -u $(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "CREATE USER IF NOT EXISTS '$(MYSQL_USER)'@'localhost' IDENTIFIED BY '$(MYSQL_PASSWORD)';"
	-@mysql -u $(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "GRANT ALL PRIVILEGES ON $(MYSQL_DATABASE).* TO '$(MYSQL_USER)'@'localhost';"
	-@mysql -u $(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "GRANT ALL PRIVILEGES ON test_student_db.* TO '$(MYSQL_USER)'@'localhost';"
	-@mysql -u $(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "FLUSH PRIVILEGES;"

# Reset the Alembic version table in MySQL (if it exists)
reset_alembic_version:
	@echo "Resetting Alembic version in the production database"
	@mysql -u $(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "USE $(MYSQL_DATABASE); DROP TABLE IF EXISTS alembic_version;"

# Initialize Alembic (if not already done)
init_migrations:
	@if [ ! -d "migrations" ]; then \
		echo "Initializing Alembic migrations"; \
		FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db init; \
	fi

# Generate migration based on models.py schema (tracks changes in schema)
generate_migration:
	@echo "Generating Alembic migration"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db migrate -m "Schema changes1-dropped column"

# Apply database migrations (runs upgrade)
apply_migration:
	@echo "Applying database migrations"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) -m flask db upgrade 

# Start Flask application
start_app:
	@echo "Starting Flask Application"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) app.py

# Resume Flask application without setup (useful for restarting the server after it has already been set up)
resume_app:
	@echo "Resuming Flask Application"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(DB_URL) $(PYTHON) app.py

# Create MySQL test database if it doesn't exist
create_test_db:
	@echo "Creating MySQL test database"
	@mysql -u $(MYSQL_ROOT_USER) -p$(MYSQL_ROOT_PASSWORD) -e "CREATE DATABASE IF NOT EXISTS test_student_db;"

# Run tests using pytest and ensure test database exists
run_tests: create_test_db
	@echo "Running tests"
	FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=$(TEST_DB_URL_ENV) $(PYTHON) -m pytest --disable-warnings

# The 'all' target that runs everything in order
all: install_dependencies create_db init_migrations generate_migration apply_migration start_app

# Cleanup target to remove virtual environment and generated files (but not migrations)
clean:
	rm -rf $(VENV_DIR) __pycache__/ .pytest_cache__/ *.db *.log

# Full clean, including migrations (use with caution)
full_clean: clean
	rm -rf migrations/