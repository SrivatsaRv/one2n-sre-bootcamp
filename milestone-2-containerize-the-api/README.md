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


## Test Schema Migraiton with Alembic Tracking Changes
- We will carry out the following actions in the code block below , ensure flask is running
- Output from a demo carried out , is also attached so you can validate 


**Step 1** - Verify your schema before changing anything 
```
mysql -u youruser -p -e "USE student_db; DESCRIBE student;"
mysql> describe student;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int          | NO   | PRI | NULL    | auto_increment |
| name  | varchar(100) | NO   |     | NULL    |                |
| age   | int          | NO   |     | NULL    |                |
| grade | varchar(20)  | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
```

**Step 2** - Replace your models.py file with below - this will simluate a schema change ( 1 new field )
```
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  # New email field

    def __repr__(self):
        return f"<Student {self.name}>"
```
**Step 3** - Generate an Alembic Migration File

```
$ make generate_migration  #This runs flask db migrate -m "Initial migration"

Generating Alembic migration
FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=mysql://youruser:yourpassword@localhost/student_db   venv/bin/python -m flask db migrate -m "Schema changes"
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'student.email'
  Generating /Users/admin/one2n-sre-bootcamp/milestone-1-create-a-rest-api/migrations/versions/cba53257b046_schema_changes.py ...  done

```

**Step 4** - Apply that Migration to Database so it can Reflect

```
$make apply_migration   #This runs flask db upgrade 

Applying database migrations
FLASK_APP=app.py FLASK_ENV=development DATABASE_URL=mysql://youruser:yourpassword@localhost/student_db   venv/bin/python -m flask db upgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> cba53257b046, Schema changes

```
**Step 4** - Verify the Database is now Showing Updated Schema for Student Table
```
>mysql USE student_db; 
>mysql DESCRIBE student;"

mysql> describe student;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int          | NO   | PRI | NULL    | auto_increment |
| name  | varchar(100) | NO   |     | NULL    |                |
| age   | int          | NO   |     | NULL    |                |
| grade | varchar(20)  | NO   |     | NULL    |                |
| email | varchar(120) | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+

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