# Milestone-4: Setup CI Pipeline with GitHub Actions

This project sets up a CI pipeline using GitHub Actions. The pipeline performs tasks such as environment setup, running lint checks, executing tests, and building and pushing Docker images to DockerHub. Additionally, the workflow can be manually triggered through GitHub's UI.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Clone the Repository](#step-1-clone-the-repository)
- [Step 2: Configure GitHub Secrets](#step-2-configure-github-secrets)
- [Step 3: Create the Workflow](#step-3-create-the-workflow)
- [Step 4: Set Up Environment](#step-4-set-up-environment)
- [Step 5: Run the Workflow Manually](#step-5-run-the-workflow-manually)
- [Step 6: Monitor the Pipeline](#step-6-monitor-the-pipeline)
- [Common Issues](#common-issues)
- [Conclusion](#conclusion)

## Prerequisites

Before getting started, ensure you have the following prerequisites:

- Git installed on your machine
- Docker installed and running
- A GitHub account with **write access** to the repository
- A GitHub Actions self-hosted runner or access to GitHub-hosted runners
- If you are on a macbook  - the keychain utils is triggered , during a login to dockerhub
- Python installed on your local machine

### Required Tools
- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python**: [Install Python](https://www.python.org/downloads/)
- **GitHub Account**: Sign up at [GitHub](https://github.com)


## How to Run ?

**Step-1**: Clone the Repository
```
$git clone https://github.com/SrivatsaRv/one2n-sre-bootcamp/
$cd one2n-milestone-4/milestone-4/setup-ci-pipeline
```


**Step-2**: Setup your Env File
```
# .env file for MySQL and Flask API
MYSQL_ROOT_PASSWORD=<password>
MYSQL_DATABASE=<name-your-db-here>
DB_URL=mysql://root:<password>@${DB_HOST}:3306/<name-your-db-here>

# docker related stuff
DOCKERHUB_TOKEN=<generated-dockerhub-token>
DOCKERHUB_USERNAME=<docker-token>
KEYCHAIN_PASSWORD=<your mac passwords>  / do this only if you have a mac,  if yes - script will pick it up.
```


**Step-3**: Setup Virtual Environment and Activate It
```
$make venv_setup 
$source venv/bin/activate
```


**Step-4**: Run the Workflow Manually with Workflow Dispatcher (or) Run a Dummy Commit -> Push
```
$git add <file-you-dummy-changed>
$git commit -m <message>
$git push -u origin milestone-4/setup-ci-pipeline
```

## Pipeline - Triggers - Here
An example run on the workflow , looks like this


**Running the Full Pipeline Manually with Makefile**: Test Setup Locally ( Makefile Only - make ci_pipeline )
```
$make venv_setup 
$source venv/bin/activate

$make ci_pipeline

(venv) admin@SrivatsaRV milestone-4-setup-ci-pipeline % make ci_pipeline
Using environment variables from .env file

Starting MySQL container using Docker Compose
[+] Running 1/1
 ✔ Container mysql_container  Started   


Running code linting with flake8...
/Users/admin/one2n-sre-bootcamp/milestone-4-setup-ci-pipeline/venv/bin/flake8 app.py tests/test_app.py models.py


Running tests using test_student_db...

=============test session starts ============
platform darwin -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/admin/one2n-sre-bootcamp/milestone-4-setup-ci-pipeline
configfile: pytest.ini
collected 8 items                                                                                                                                     

tests/test_app.py ........                                                                                                     [100%]

================ 8 passed in 0.34s ===========


Building Flask API Docker image with version 1.6.0  ...
[+] Building 2.1s (19/19) FINISHED
docker:desktop-linux

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/j2pyvq4lrhe5jivwxilsrmfc7
Logging in to DockerHub...
Running on macOS, unlocking keychain...
Login Succeeded
Pushing Docker image to DockerHub...
The push refers to repository [docker.io/srivatsarv21/one2n-bootcamp]

 ```

