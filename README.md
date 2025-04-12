# Student API

A student CRUD REST API using Python and Flask.

## Functional Requirements

This API provides the following operations:

1. Add a new student.
2. Get all students.
3. Get a student by ID.
4. Update existing student information.
5. Delete a student record.

## Pre-requisites

Ensure the following tools are installed on your system:

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/
- Make: https://www.gnu.org/software/make/

## Setup Instructions

### 1. Build and Run the API

1. **Clone the repository:**
    ```bash
    git clone git@github.com:chhaya1/student-REST-API.git
    cd student-REST-API
    ```

2. **Create your `.env` file:**
    Add configurations such as database credentials:
    ```bash
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=
    DATABASE_URL=
    ```

3. **Build and run the application using Docker Compose:**
    ```bash
    make run
    ```

    This command will:
    - Start the PostgreSQL database container.
    - Initialize migrations.
    - Apply migrations to the database.
    - Build and run the REST API container.

4. **Access the API:**
    The API will be available at `http://localhost:5000`.

    Use an API client (e.g., Postman or curl) to interact with the API endpoints.

### 2. Manage Database Migrations

The following `Makefile` targets will help with database migrations:

- **Initialize migrations folder:**
    ```bash
    make init-migrations
    ```

- **Generate migration script each time the model is updated:**
    ```bash
    make migrate-db
    ```

- **Apply migrations to the database:**
    ```bash
    make upgrade-db
    ```

### 3. Running the API and Database

- To **start the database** without starting the API:
    ```bash
    make start-db
    ```

- To **build and run the API** without running the database:
    ```bash
    make build-api
    make run-api
    ```

## API Endpoints

The following endpoints are available in the API:

1. **Healthcheck**
   - `GET /api/v1/healthcheck`
   - Example response: `{"status": "healthy"}`

2. **Get all students**
   - `GET /api/v1/students`
   - Example response:
     ```json
     [
       {"id": 1, "name": "Chhaya", "age": 21, "major": "Computer Science"},
       {"id": 2, "name": "Harshita", "age": 22, "major": "Mathematics"}
     ]
     ```

3. **Get a student by ID**
   - `GET /api/v1/students/{id}`
   - Example response:
     ```json
     {"id": 1, "name": "Chhaya", "age": 21, "major": "Computer Science"}
     ```

4. **Add a new student**
   - `POST /api/v1/students`
   - Example request:
     ```json
     {"name": "Chhaya", "age": 21, "major": "Computer Science"}
     ```
   - Example response:
     ```json
     {"id": 1, "name": "Chhaya", "age": 21, "major": "Computer Science"}
     ```

5. **Update a student**
   - `PUT /api/v1/students/{id}`
   - Example request:
     ```json
     {"name": "Harshita", "age": 25, "major": "Mathematics"}
     ```
   - Example response:
     ```json
     {"id": 1, "name": "Harshita", "age": 25, "major": "Mathematics"}
     ```

6. **Delete a student**
   - `DELETE /api/v1/students/{id}`
   - Example response:
     ```json
     {"message": "Student deleted successfully"}
     ```


## GitHub Actions CI Pipeline

This project uses GitHub Actions for continuous integration. The pipeline is defined in `.github/workflows/docker-build.yml`. It performs the following steps:

### Workflow Triggers

The pipeline is triggered by a push to the `main` branch.

### Pipeline Jobs

The pipeline consists of the following steps:

1. **Checkout the Code**:
   - The repository is cloned using the `actions/checkout@v3` action.

   ```
   git clone https://github.com/chhaya1/student-REST-API.git
   ```
2. **Set up Python 3.9**:

The Python environment is set up using the actions/setup-python@v3 action.

```
sudo apt-get install python3.9
```

3. **Install Dependencies**:

The pipeline installs the required Python dependencies from requirements.txt and the linting tool pylint.
Bash Equivalent:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pylint
```

4. **Perform Linting**:

The code is checked for style and syntax errors using pylint.

```
make lint
```

5. **Set up Docker Buildx**:

Docker Buildx is set up using the docker/setup-buildx-action@v2 action to build and push multi-platform Docker images.

6. **Log in to DockerHub**:

Create an account on DockerHub and DockerHub login is performed using the docker/login-action@v2. It uses GitHub Secrets to store the DockerHub credentials:

DOCKER_USERNAME
DOCKER_PASSWORD

```
echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
```

7. **Build and Push Docker Image**:

The Docker image is built and pushed to DockerHub using a Makefile command. The image is tagged as chhaya786/student-api:1.0.1.

```
make docker-push
```

8. **Environment Variables**:
The following environment variables are used in the GitHub Actions pipeline:

DOCKER_USERNAME: DockerHub username stored as a GitHub secret.
DOCKER_PASSWORD: DockerHub password stored as a GitHub secret.
DOCKER_IMAGE: The image name and version used to tag the Docker image (e.g., chhaya786/student-api:1.0.1).

9. **Adding Secrets to GitHub**
Ensure that your DockerHub credentials (DOCKER_USERNAME and DOCKER_PASSWORD) are stored as GitHub secrets:

Go to your repository on GitHub. Click on Settings > Secrets and variables > Actions.

Add the following secrets:
DOCKER_USERNAME: Your DockerHub username.
DOCKER_PASSWORD: Your DockerHub password.


## Setting up GitHub Actions Runner (Self-hosted)

This project uses a self-hosted GitHub Actions runner to execute the CI pipeline. Follow these steps to install, configure, and start a GitHub Actions runner on your own infrastructure.

### Prerequisites

- A server or VM with at least 2 CPU cores and 4 GB of RAM.
- Ubuntu (preferred) or any compatible Linux distribution.
- `Docker` and `Python` should be installed on the runner machine.

### Step 1: Install Docker

If Docker is not installed, you can install it using the following commands:

```
# Update the package index
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Start Docker
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker
```

### Step 2: Install Python 3.9 (if not installed)

If Python 3.9 is not already installed, run the following commands:

```
sudo apt-get update
sudo apt-get install -y python3.9 python3-pip
```

### Step 3: Download and Configure GitHub Actions Runner

Download the runner: 
Go to your repository on GitHub, navigate to Settings > Actions > Runners, and follow the instructions to create a self-hosted runner. The specific download URL and token will be provided by GitHub.

Here is an example of how to download and configure the runner:

```
# Navigate to a folder to install the runner
mkdir actions-runner && cd actions-runner

# Download the latest runner package (replace the URL with the one GitHub provides)
curl -o actions-runner-linux-x64-2.292.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.292.0/actions-runner-linux-x64-2.292.0.tar.gz

# Extract the installer
tar xzf ./actions-runner-linux-x64-2.292.0.tar.gz
```

# Configure the runner: Register the runner with your repository using the registration token that GitHub provides:

```
# Replace the URL with your repository URL and token from GitHub
./config.sh --url https://github.com/yourusername/yourrepo --token YOUR_TOKEN_HERE
```

The --url should point to your GitHub repository.
The --token is a registration token from the GitHub repository's runner setup page.

### Step 4: Start the GitHub Actions Runner
After the runner is configured, you need to start the runner service. You can run it in the foreground or as a service.

Run the runner in the foreground (for testing):

```
./run.sh
```

### Step 5: Verify the Self-hosted Runner

Once the runner is started, it should appear as Online in the Settings > Actions > Runners section of GitHub repository.

You can now trigger your GitHub Actions workflows, and they will run on your self-hosted runner.


##  Setup Instructions for Kubernetes cluster set up with minikube, Vault (secret management) and Kubernetes External secrets store operator
1. Start Minikube with 3 nodes

```
minikube start --nodes=3
```

2. Verify all nodes are ready
```
kubectl get nodes
3. Label the nodes
```
```
kubectl label node minikube-m02 type=application
kubectl label node minikube-m03 type=database
kubectl label node minikube-m04 type=dependent_services
```
4. Confirm the labels
```
kubectl get nodes --show-labels
```
5. Create Kubernetes manifests (yml files) for Application and deoploy it.

```
kubectl apply -f k8s/student-api/application.yml
```
6. Create Kubernetes manifests (yml file) for database and deploy the Database (with Init Container for DB Migrations)

```
kubectl apply -f k8s/database/database.yml
```

7. Install HashiCorp Vault in Dev Mode Using Helm on Kubernetes
   1. Add the HashiCorp Helm repo
      ```
      helm repo add hashicorp https://helm.releases.hashicorp.com
      helm repo update
      ```
   2. Install Vault in dev mode using Helm
      ```
      helm install vault hashicorp/vault \
      --set "server.dev.enabled=true"
      ```
      This deploys Vault in dev mode, which is already unsealed by default

      Generates a new root token each time it's started

      Stores data in-memory only (non-persistent) which is meant for testing/dev only

   3. Verify that the Vault pod is running
      ```
      kubectl get pods -n default
      ```

   4. Check Vault logs to get the root token
      ```
      kubectl logs vault-0
      ```
      Look for the root token in the logs:

      ==> Vault server started! Log data will stream in below:
      ...
      Root Token: s.xxx

8. Install External Secrets Operator (ESO) 
   1. Add the External Secrets Helm repo
      ```
      helm repo add external-secrets https://charts.external-secrets.io
      helm repo update
      ```
   2. Create the external-secrets namespace
      ```
      kubectl create namespace external-secrets
      ```
   3. Install the External Secrets Operator using Helm
      ```   
      helm install external-secrets external-secrets/external-secrets \
      --namespace external-secrets
      ```
      This installs the ESO controller in the specified namespace.

   4. Verify the ESO pods are running
      ```
      kubectl get pods -n external-secrets
      ```


9. Connect ESO to HashiCorp Vault
   1. Enable Kubernetes auth method in Vault
      ```
      kubectl exec -it <vault-pod> -- /bin/sh
      ```
      Then run these commands inside the Vault shell:
      ```
      vault auth enable kubernetes
      ```

10. Create secrets in Vault:
    ```
    vault kv put secret/db password=postgres
    ```

11. Configure External Secrets to Use Vault

    ```
    kubectl apply -f cluster-secret-store.yml
    ```


Make sure the Kubernetes ExternalSecret resource points to the Vault key paths.

## Accessing the API

1. Check the deployment done successfully:

   ```
   kubectl get pods -n student-api
   ```

   After successful deployment, check service account
   ```
   kubectl get svc -n student-api
   ```
2. Test the API working
   ```
   curl http://localhost:5000/api/v1/students
   ```

### Set up of Helm and Deployment using Helm

1. Create a new Helm chart for the application
```
mkdir helm
cd helm
helm create student-api
```

2. Pull Required Charts (for PostgreSQL & Vault)

# Add Helm repositories
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add hashicorp https://helm.releases.hashicorp.com
```

# Pull charts into your helm directory
```
helm pull bitnami/postgresql --untar --untardir helm/
helm pull hashicorp/vault --untar --untardir helm/
```

3. Configure values.yaml
Before deploying, update the following values inside helm/student-api/values.yml

4. Render and Validate the Helm Template
```
helm template helm/student-api
```
This command renders your Kubernetes YAML files locally without applying them, helping you catch errors early.

6. Deploy to Kubernetes
```
helm upgrade --install student-api helm/student-api
```




