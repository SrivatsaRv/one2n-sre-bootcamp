# Milestone 2 - Containerizing the REST API

### Prerequisites
Make sure you have the following installed on your machine:
- Docker version 27.1.1 or equivalent 
- Python 3.12 or higher
- Make: Install Make Tool 
- pip3: Python package manager
- Requirements.txt file - (especially flask)

### Step 1 - Clone the Repository 
```
git clone https://github.com/SrivatsaRv/one2n-sre-bootcamp.git \
cd one2n-sre-bootcamp/milestone-2-containerize-the-api
```

### Step 2 - Setup your Local Venv (trust me , you need this)

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 -m flask --version
python3 -m alembic --version
```

### Step 3 - Prepare for Migration Capability (Used for applying schema when DB comes up)
```
python3 -m flask db init   #initialize Alembic Migration Directory
python3 -m flask db migrate -m "Creating table from models.py schema file"  #generates migration file
python3 -m flask db upgrade    # Propogates the changes from models.py source code -> database container
```

### Step 4 - Run the final Make command 
```
make all
```

## Tech Stack
- **Code and Framework** - Python + Flask
- **ORM + Database + Migration Tool**  - SQL Alchemy + MySQL + Alembic 


## Endpoints that will go live once you run it - 
- `GET /api/v1/healthcheck` - returns status as healthy
- `GET /api/v1/students` - get all students
- `GET /api/v1/students/<int:id>` - get students by ID
- `POST /api/v1/students` - insert new student record
- `PUT /api/v1/students/<int:id>` - update student record by ID
- `DELETE /api/v1/students/<int:id>` - delete student record by ID

## Folder Structure Includes - 
- `app.py:` Main Flask app file.
- `models.py:` Schema definitions for the database.
- `requirements.txt:` List of dependencies.
- `migrations/:` Alembic migrations folder.
- `tests/:` Unit tests, e.g., test_app.py.

## Milestone Status 
- API should be run using the docker image. - ✅
- Dockerfile should have different stages to build and run the API. - ✅
- We should be able to inject environment variables while running the docker container at runtime. - ✅
- README.md should be updated with proper instructions to build the image and run the docker container. - ✅
- Similarly appropriate make targets should be added in the Makefile. - ✅
- The docker image should be properly tagged using semver tagging, use of latest tag is heavily discouraged. - ✅
- Appropriate measures should be taken to reduce docker image size. We want our images to have a small size footprint. - ✅
