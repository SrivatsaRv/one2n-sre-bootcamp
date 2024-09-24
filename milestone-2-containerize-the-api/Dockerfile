# Stage 1: Build the application in a lightweight Python image
FROM python:3.12-slim AS build-stage

# Set environment variables
ENV PYTHONUNBUFFERED=1 \  
    PIP_NO_CACHE_DIR=1 

# Create and set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code into the container
COPY . .

# Stage 2: Use a minimal image for running the app
FROM python:3.12-alpine AS runtime-stage

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create and set the working directory inside the container
WORKDIR /app

# Copy the installed dependencies and source code from the build stage
COPY --from=build-stage /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build-stage /app /app

# Expose port 5000 for Flask
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
