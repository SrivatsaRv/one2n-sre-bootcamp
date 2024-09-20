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

# Start Flask application in the background
start_app: install_dependencies
	@echo "Starting Flask Application"
	@$(PYTHON) app.py &

# Check healthcheck endpoint and validate status code
check_app_running:
	@sleep 5  # Wait for app to start
	@echo "Checking healthcheck status"
	@curl -f -s -o /dev/null http://127.0.0.1:5000/healthcheck && echo "API is healthy" || (echo "Healthcheck failed"; exit 1)

# Add the target to run tests using pytest
test:
	@echo "Running tests"
	PYTHONPATH=. venv/bin/python -m pytest -v tests/


# The 'all' target that runs everything in order
all: setup_venv install_dependencies start_app check_app_running

# Cleanup target to remove virtual environment and generated files
clean:
	rm -rf $(VENV_DIR) instance/*.db *.log