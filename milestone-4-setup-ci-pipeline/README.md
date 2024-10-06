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
- Python installed on your local machine

### Required Tools

- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python**: [Install Python](https://www.python.org/downloads/)
- **GitHub Account**: Sign up at [GitHub](https://github.com)