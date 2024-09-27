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
make venv_setup   #activates a venv to download a few dependencies
source venv/bin/activate

```

### Step 3 - Bring up Database Container
```
$make run_db   # your db container should be up by now and running (db created , schema yet to be applied)
```

### Step 4 - Initialize Alembic Directory and Generate a Migration File
```
$make init_migrations   #initiates alembic , and brings up migrations/ folder

$make generate_migration   # generates the schema migration file , can be applied to database
```

### Step 5 - Apply the Migration to Database
```
$make apply migration    #applies the action items in schema migration file
$make verify_db    #prints table schema for student table , in student_db database
```

### Step 6 - Bring up Flask Application Container
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
