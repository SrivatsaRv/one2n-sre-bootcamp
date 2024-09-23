# Milestone 1 - Creating a Simple REST API
All SRE Bootcamp Progress will be tracked here, goal is to complete the below milestones - with clarity , and implement best practices and production grade setup. 

## Instructions to Run 
### Prerequisites
Make sure you have the following installed on your machine:

- Python 3.12 or higher
- Make: Install Make Tool 
- pip: Python package manager
- MySQL - Version 9.0.1 or lower

### Step 1 - Clone the Repository 
`git clone https://github.com/SrivatsaRv/one2n-sre-bootcamp.git`\
`cd one2n-sre-bootcamp/milestone-1-create-a-rest-api`

### Step 2 - Run Make Command to Setup Webserver
`/one2n-sre-bootcamp/milestone-1-create-a-rest-api - make all` - Wait for server to come up

### Step 3 - Run Unit Tests for API 
`/one2n-sre-bootcamp/milestone-1-create-a-rest-api - make run_tests` - All tests will pass here

### Step 4 - Test Schema Migraiton with Alembic Tracking Changes
- We will carry out the following actions in the code block below , ensure flask is running

```
mysql -u youruser -p -e "USE student_db; DESCRIBE student;"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # New email field added here

flask db migrate -m "Add email field to Student" 

flask db upgrade

mysql -u youruser -p -e "USE student_db; DESCRIBE student;"
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
**Underway** - Create a simple REST API Webserver - - The repository should contain the following
- Create a public repository on GitHub - ✅
- README.md file explaining the purpose of the repo, along with local setup instructions - ✅
- Explicitly maintaining dependencies in a file ex (requirements.txt and Makefile in our case) - ✅
- Makefile to build and run the REST API locally. - ✅
- Ability to run DB schema migrations to create the student table. - ✅
- Config (such as database URL) should not be hard-coded in the code and should be passed through   environment variables. - ✅
- Postman collection for the APIs. - ✅

## API expectations
- Support API versioning (e.g., api/v1/<resource>). - ✅
- Using proper HTTP verbs for different operations. - ✅
- API should emit meaningful logs with appropriate log levels. - ✅
- API should have a /healthcheck endpoint - ✅
- Unit tests for different endpoints - ✅


## Future improvements - 
- **Logging Perspective** - If the API server goes down , the app.log file exists - new instance should log to same file. 
- **SSL Certificate for the HTTP Application** - Install self-signed certificates
- **Authenticated Requests** - Using a simple auth (Basic Auth on Postman) initially to validate incoming requests, only then serve