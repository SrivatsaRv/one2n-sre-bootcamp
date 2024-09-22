# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

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

# Initialize Alembic (if not already done)
init_migrations:
	@if [ ! -d "migrations" ]; then \
		echo "Initializing Alembic migrations"; \
		$(PYTHON) -m flask db init; \
	fi

# Run database migrations (apply migration if not up-to-date)
migrate_db: init_migrations
	@echo "Applying database migrations"
	@$(PYTHON) -m flask db upgrade

# Generate migration (to track model changes)
generate_migration: migrate_db
	@echo "Generating Alembic migration"
	@$(PYTHON) -m flask db migrate -m "Applying schema from models.py"

# Start Flask application in the background
start_app: install_dependencies migrate_db
	@echo "Starting Flask Application"
	@$(PYTHON) app.py &

# The 'all' target that runs everything in order
all: install_dependencies migrate_db start_app

# Cleanup target to remove virtual environment and generated files
clean:
	rm -rf $(VENV_DIR) instance/*.db *.log