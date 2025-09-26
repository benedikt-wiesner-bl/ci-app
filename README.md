
# ci-app

A lightweight **CI/CD and monitoring lab** with Jenkins, a ToDo app (Python/Flask), Prometheus, Grafana, cAdvisor, Dozzle – and integrated **security scanning with Trivy**.
Everything runs via `Docker` and `docker compose` on your local machine.

---

## Features

- **CI/CD with Jenkins**
  Use Jenkins with a `Jenkinsfile` to automatically build, test, and perform **blue-green deployments** of your app.

- **Python ToDo App**
  Small Flask application with SQLite as an example project.
  - Runs internally as two containers (`ci-app-blue` and `ci-app-green`)
  - Jenkins switches between both versions via Nginx → **zero-downtime deployment**

- **Monitoring & Logging**
  - `Prometheus` collects metrics
  - `Grafana` visualizes dashboards
  - `cAdvisor` shows container resources
  - `Dozzle` provides logs of all containers in the browser

- **Security Scanning**
  Jenkins pipelines run **Trivy** container and dependency scans to identify known vulnerabilities.

- **Unified Environment**
  Everything is defined in `docker-compose.yml`, with persistent volumes for Jenkins, Grafana, and Prometheus.

- **UI Convenience**
  Your ToDo app includes footer links to all services → no more port hunting.

---

## Installation & Setup

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/) (included with Docker Desktop)

### Steps

1. **Clone Repository**

```bash
git clone https://github.com/benedikt-wiesner-bl/ci-app.git
cd ci-app
```

2. **Start Services**

```bash
docker compose -f config/docker-compose.yml up --build -d
```

This builds the images and starts all services in the background.
On first start, Jenkins may take a few minutes.

3. **Access Services in Browser**

- **ToDo App (always via Nginx)** → [http://localhost:8085](http://localhost:8085)
- **Jenkins** → [http://localhost:8080](http://localhost:8080)
  - Initial admin password:
    ```bash
    docker logs jenkins | grep "initialAdminPassword"
    ```
- **Grafana** → [http://localhost:3000](http://localhost:3000)
  - Login: `admin` / `admin` (change password on first login)
- **Prometheus** → [http://localhost:9090](http://localhost:9090)
- **cAdvisor** → [http://localhost:8081](http://localhost:8081)
- **Dozzle (Logs)** → [http://localhost:9999](http://localhost:9999)

---

## CI/CD with Blue-Green & Security Scan

Your `Jenkinsfile` contains several stages:

1. **Build**
   Builds the Python ToDo app as a Docker image.

2. **Test**
   Runs unit tests (e.g., with `pytest`).

3. **Security Scan (Trivy)**
   Scans the built Docker image and your dependencies for vulnerabilities.

4. **Deploy (Blue-Green)**
   - Jenkins deploys the new version into an inactive container (`blue` or `green`).
   - Runs a healthcheck (`/health`).
   - Switches Nginx to the new version → the old version remains available for rollback.

---

## Local Development of the App

The app is designed for Docker, but can also run locally:

```bash
cd app
pip install -r requirements.txt
python __init__.py
```

→ then it runs on [http://localhost:5000](http://localhost:5000) (local only, without Nginx).

---

## Folder Structure

```
ci-app/
│── app/                 # Flask ToDo app
│   └── templates/       # HTML templates (base.html, index.html)
│── config/              # docker-compose.yml, nginx, Jenkinsfile, prometheus.yml
│   └── nginx/           # Nginx config
│── data/                # SQLite database (todos.db)
│── grafana/             # Grafana provisioning & dashboards
│── infrastructure/      # Dockerfiles for Jenkins and app
│── jenkins_ss/          # SSH keys & config for Jenkins
│── scripts/             # Helper scripts (backup.sh, boot.sh)
│── tests/               # Unit tests for the app
│── .dockerignore
│── .gitignore
│── README.md
│── requirements.txt
```
