## Milestone-3 - One Click Local Deployment Step

**Goal** - To get the environment setup and running in the least amount of steps possible. 


### Prerequisites
Make sure you have the following installed on your machine:
- Docker version 27.1.1 or equivalent 
- Python 3.12 or higher
- Make: Install Make Tool 
- pip3: Python package manager
- Requirements.txt file - (especially flask)

### Step 0 - Prepare your .env file in the Project Directory
```
#NOTE - Have a .env file that has the following format - 

MYSQL_ROOT_PASSWORD=<password>
MYSQL_DATABASE=student_db
DB_URL=mysql://root:<password>@{DB_HOST}:3306/student_db
```

### Step 1 - Clone the Repository and Activate Venv
```
git clone https://github.com/SrivatsaRv/one2n-sre-bootcamp.git \
cd one2n-sre-bootcamp/milestone-3-airplane-mode

$make venv_setup
$source venv/bin/activate
```

### Step 2 - Run the Makefile Targets 
```
$make all
```

### Actions in the Makefile will run the following steps - 
```
- Run DB Container 
- Run DB DML Migrations 
- Build New Docker Image 
- Run New Container 
- Run Tests 
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

### When we run the make target to start the REST API docker container
    - It should first start the DB and run DB DML migrations - ✅ 
    - (Good to have) You can even include checks to see if the DB is already running and DB migrations are already applied. - ✅
    - Later it should invoke the docker compose command to start the API docker container.  (fulfilled by compose seutp, and entrypoint -> cmd) - ✅
