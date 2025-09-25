# ci-app 🚀

A robust CI/CD pipeline and application deployment environment, powered by Jenkins, Docker, and integrated monitoring.

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-None-lightgrey) ![Stars](https://img.shields.io/github/stars/benedikt-wiesner-bl/ci-app?style=social) ![Forks](https://img.shields.io/github/forks/benedikt-wiesner-bl/ci-app?style=social)

## ✨ Features

*   **Automated CI/CD Pipeline**: ⚙️ Leverage `Jenkins` and `Jenkinsfile` for continuous integration and continuous deployment, ensuring rapid and reliable software delivery.
*   **Containerized Environment**: 🐳 Deploy and manage all services, including the application, Jenkins, Prometheus, and Grafana, using `Docker` and `docker-compose.yml` for consistency and isolation.
*   **Integrated Monitoring**: 📊 Gain deep insights into your application and infrastructure performance with `Prometheus` for metrics collection and `Grafana` for powerful visualization dashboards.
*   **Python Application Backend**: 🐍 A modular Python application (`app/`) ready for development, testing, and deployment within the CI/CD ecosystem.
*   **Comprehensive Testing**: ✅ Includes a dedicated `tests/` directory to ensure code quality and functionality throughout the development lifecycle.


## 🚀 Installation Guide

Follow these steps to get `ci-app` up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

*   [Git](https://git-scm.com/)
*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker Desktop)

### Step-by-Step Setup

1.  **Clone the Repository**
    Start by cloning the `ci-app` repository to your local machine:

    ```bash
    git clone https://github.com/benedikt-wiesner-bl/ci-app.git
    cd ci-app
    ```

2.  **Build and Start Services with Docker Compose**
    The `docker-compose.yml` file defines all the necessary services, including Jenkins, Prometheus, Grafana, and the Python application.

    ```bash
    docker-compose up --build -d
    ```
    This command will:
    *   Build the Docker images for your services (including the Python app).
    *   Start all services in detached mode (`-d`).
    *   It might take a few minutes for all services, especially Jenkins, to fully initialize.

3.  **Access Services**
    Once the services are running, you can access them via your web browser:
    *   **Jenkins**: `http://localhost:8080`
        *   You'll need to retrieve the initial admin password from the Jenkins container logs:
            ```bash
            docker logs jenkins-master | grep "initialAdminPassword"
            ```
            Follow the Jenkins setup wizard to install recommended plugins and create your first admin user.
    *   **Grafana**: `http://localhost:3000`
        *   Default login: `admin`/`admin` (you'll be prompted to change it).
    *   **Prometheus**: `http://localhost:9090`
    *   **Python Application**: `http://localhost:5001` (or as configured in `app/`)

4.  **Configure Jenkins (Optional but Recommended)**
    *   Once Jenkins is set up, you can create a new pipeline job and point it to the `Jenkinsfile` in your repository. This will automatically set up your CI/CD pipeline.


## 💡 Usage Examples

### Running the Python Application Locally (outside Docker)

While the application is designed to run within Docker, you can run it locally for development purposes.

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**
    ```bash
    python app/__init__.py # Or your main application entry point
    ```
    The application should then be accessible at `http://localhost:5001` (or its configured port).

### Triggering a Jenkins Pipeline

1.  Navigate to your Jenkins dashboard (`http://localhost:8080`).
2.  If you've set up a pipeline job for `ci-app`, click on it.
3.  Click "Build Now" to manually trigger a build of your CI/CD pipeline.

### Viewing Monitoring Dashboards in Grafana

1.  Access Grafana at `http://localhost:3000`.
2.  Log in with `admin`/`admin` (and change password).
3.  Explore the pre-configured Prometheus data source.
4.  Import or create new dashboards to visualize metrics from your application and Jenkins.


