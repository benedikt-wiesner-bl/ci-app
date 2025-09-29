# ci-app

A lightweight **CI/CD and monitoring lab** with Jenkins, a ToDo app (Python/Flask), Prometheus, Grafana, cAdvisor, Dozzle – and integrated **security scanning with Trivy**.
Everything runs via **Docker** and **docker compose** on your local machine.

---

## Features

- **CI/CD with Jenkins**
  Use Jenkins with a `Jenkinsfile` to automatically build, test, and perform **blue‑green deployments** of your app.

- **Python ToDo App**
  Small Flask application with SQLite as an example project.
  - Runs internally as two containers (`ci-app-blue` and `ci-app-green`)
  - Jenkins switches between both versions via Nginx → **zero‑downtime deployment**

- **Monitoring & Logging**
  - `Prometheus` collects metrics
  - `Grafana` visualizes dashboards
  - `cAdvisor` shows container resources
  - `Dozzle` provides logs of all containers in the browser

- **Security Scanning**
  Jenkins pipelines run **Trivy** container and dependency scans to identify known vulnerabilities.
  HTML reports are generated using a custom template.

- **Unified Environment**
  Everything is defined in `config/docker-compose.yml`, with persistent volumes for Jenkins, Grafana, and Prometheus.

- **UI Convenience**
  Your ToDo app includes footer links to all services → no more port hunting.
---

## Security Reports

Trivy generates HTML reports during the Jenkins pipeline.
Reports are stored in the Jenkins workspace under `trivy-report/` and published in the Jenkins UI.

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

Using docker compose directly:

```bash
docker compose -f config/docker-compose.yml up --build -d
```

This builds the images and starts all services in the background.
On first start, Jenkins may take a few minutes.

**—or—** use the provided helper script (especially handy on WSL):

```bash
./scripts/boot.sh -build   # first time: starts Docker service and builds/starts all services
./scripts/boot.sh -start   # subsequent starts
./scripts/boot.sh -stop    # stop all services
```

3. **Access Services in Browser**

- **ToDo App (via Nginx)** → <http://localhost:8085>
- **Jenkins** → <http://localhost:8080>
  Initial admin password:
  ```bash
  docker logs jenkins | grep "initialAdminPassword"
  ```
- **Grafana** → <http://localhost:3000>
  Login: `admin` / `admin` (change password on first login)
- **Prometheus** → <http://localhost:9090>
- **cAdvisor** → <http://localhost:8081>
- **Dozzle (Logs)** → <http://localhost:9999>

---

## Required Jenkins Plugins

For the pipeline to run, the following plugins must be installed in Jenkins:

- **Pipeline** (Workflow: Aggregator)
- **Pipeline: Git** / **GitHub** (for `git` checkout with credentials)
- **Docker Pipeline** (for `docker build`, `docker run`, `docker.withRegistry`, etc.)
- **HTML Publisher** (for `publishHTML`)
- **Credentials Binding** (to integrate SSH key / GitHub key)
- **AnsiColor** (optional, colored console logs)

Installation:
In Jenkins → **Manage Jenkins** → **Plugins** → **Available plugins** → search & install → restart Jenkins.

---

## CI/CD with Blue‑Green & Security Scan

Your `Jenkinsfile` contains several stages:

1. **Checkout** – Clones the GitHub repository.
2. **Code Quality** – Runs `flake8` linting.
3. **Build** – Builds the Python ToDo app as a Docker image.
4. **Test** – Runs unit tests with `pytest`.
5. **Security Scan (Trivy)** – Scans the built Docker image and dependencies; generates an **HTML security report**.
6. **Deploy (Blue‑Green)** – Deploys into the inactive container (`blue` or `green`), runs a `/health` check, then switches Nginx to the new version → enabling quick rollback.

---

## Local Development of the App

The app is designed for Docker, but can also run locally:

```bash
cd app
pip install -r requirements.txt
python __init__.py
```

Then open <http://localhost:5000> (local only, without Nginx).

---

## Folder Structure

```
ci-app/
│── app/                 # Flask ToDo app
│   └── templates/       # HTML templates (base.html, index.html)
│── config/              # docker-compose.yml, nginx config, Jenkinsfile, prometheus.yml
│   └── nginx/           # Nginx config
│   └── trivy/           # Custom Trivy HTML template (html.tpl)
│── data/                # SQLite database (todos.db)
│── grafana/             # Grafana provisioning & dashboards
│── infrastructure/      # Dockerfiles for Jenkins and app
│── jenkins_ssh/         # SSH keys & config for Jenkins
│── scripts/             # Helper scripts (backup.sh, boot.sh)
│── tests/               # Unit tests for the app
│── .dockerignore
│── .gitignore
│── README.md
│── requirements.txt
```

