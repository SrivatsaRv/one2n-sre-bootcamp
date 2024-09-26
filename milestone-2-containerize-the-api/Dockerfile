# Stage 1: Build stage
FROM python:3.9-slim AS build-stage

# Install system dependencies for mysqlclient and other needed libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    libffi-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy only the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies using pip3
RUN pip3 install --no-cache-dir -r requirements.txt

# Stage 2: Final stage (runtime environment)
FROM python:3.9-slim

# Install the runtime dependency for mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the installed Python dependencies from the build stage
COPY --from=build-stage /usr/local/lib/python3.9 /usr/local/lib/python3.9

# Copy only necessary files from the host to the container (app.py, models.py, and .env)
COPY app.py app.py
COPY models.py models.py
COPY .env .env

# Expose the Flask port
EXPOSE 5000

# Ensure environment variables are loaded
ENV FLASK_APP=app.py

# Set the default command to run the Flask app with python3 -m flask run
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]