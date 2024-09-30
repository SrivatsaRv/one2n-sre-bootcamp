## Milestone-3 - One Click Local Deployment Step

**Goal** - To get the environment setup and running in the least amount of steps possible. 


### Prerequisites
Make sure you have the following installed on your machine:
- Docker version 27.1.1 or equivalent 
- Python 3.12 or higher
- Make: Install Make Tool 
- pip3: Python package manager
- Requirements.txt file - (especially flask)

### Step 1 - Clone the Repository and Activate Venv
```
git clone https://github.com/SrivatsaRv/one2n-sre-bootcamp.git \
cd one2n-sre-bootcamp/milestone-3-airplane-mode

$make venv_setup
$source venv/bin/activate
```

### Step 2 - Bring up Database Container (MySQL 8.0)

```
$make run_db  

#NOTE - brings up a MySQL 8.0 container with student_db database created, no tables here yet. 
```

### Step 3 - Initialize Alembic Directory and Generate a Migration File
```
#NOTE - Run init_migrations only if you do not see a migrations/ folder in your working directory 

$make init_migrations   #initiates alembic , this brings up migrations/ folder

#NOTE - .env file - should have the string  @127.0.0.1:3306/student_db (so alembic can generate the migration file locally after diff with sql container)

$make generate_migration   # generates the schema migration file under migrations/versions/<generated-migration-file>.py
```

### Step 4 - Version and Build the API Server Image 
```
#NOTE - .env file - should have the string  @mysql_container:3306/student_db (this env file is shared with container as well , which can now reference db by name (mysql_container)
#NOTE - Makefile - change the tag if you'd want it to be versioned, else keep it TAG ?=1.0.0

$make build_api  #brings up a semantic versioned Flask API image
```

### Step 6 - Decide If Migrations Should Apply / Or Not when Container Comes Up
```
#NOTE - Docker compose file , has a variable called - MIGRATIONS: "false" / "true" - depending on what you set here, the Flask API container will execute its ENTRYPOINT command

$make run_api   #brings up the Flask API container image, that will now be up and running , based on flag , migrations may or may not have been applied. 
```

### Step 6 - Decide If Migrations Should Apply / Or Not when Container Comes Up
```
#NOTE - Docker compose file , has a variable called - MIGRATIONS: "false" / "true" - depending on what you set here, the Flask API container will execute its ENTRYPOINT command

$make run_api   #brings up the Flask API container image, that will now be up and running , based on flag , migrations may or may not have been applied. 
``` 


### Verification of Schema Being Applied  - 
**Attach shell to mysql container running - and follow below steps**
```
- Inside the database container
- USE student_db;   - student_db is created by docker compose setup 
    - SHOW tables;  - 2 table should be created (alembic_versions and student) 
        - SELECT * FROM student;   - list all entries in the student table 
        - DESCRIBE student; - displays the schema , note it down
```

**Inserting Records - Killing Existing App Container - Spawning a New One**
```
    - Insert Records from Postman - (5 Records) - 
    - Kill Flask Container -> set MIGRATIONS = FALSE in docker-compose file -> rename image version from 1.0.0 to 1.1.0 , 
    - Build New Image -> Start New Container - Flask should be served again 
    - Insert Records from Postman - (5 New Records)
    - Validation - SAME DATABASE VOLUME SHOULD CONTINUE TAKING WRITES) 
```


## Milestone Expectations
- API should be run using the docker image - ✅
- API and its dependent services should be run using docker-compose - ✅

- Makefile should have the following targets.
    - To start DB container - ✅
    - To run DB DML migrations - ✅
    - To build REST API docker image - ✅
    - To run REST API docker container - ✅
- README.md file should be updated with instructions
- To add pre-requisites for any existing tools that must already be installed (e.g., docker, make, etc) - ✅
- To run different make targets and the order of execution - ✅

- When we run the make target to start the REST API docker container
    - It should first start the DB and run DB DML migrations - ✅ 
    - (Good to have) You can even include checks to see if the DB is already running and DB migrations are already applied. (applies conditionally based on MIGRATION variable) - ✅
    - Later it should invoke the docker compose command to start the API docker container.  (fulfilled by compose seutp, and entrypoint -> cmd) - ✅
