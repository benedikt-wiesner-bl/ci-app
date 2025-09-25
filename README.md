# ci-app

Ein leichtgewichtiges **CI/CD- und Monitoring-Lab** mit Jenkins, einer ToDo-App (Python/Flask), Prometheus, Grafana, cAdvisor, Dozzle – und integriertem **Security-Scanning mit Trivy**.  
Alles läuft über `Docker` und `docker compose` auf deinem lokalen Rechner.  

---

## Features

- **CI/CD mit Jenkins**  
  Nutze Jenkins mit einem `Jenkinsfile`, um deine App automatisch zu bauen, zu testen und **Blue-Green-Deployments** durchzuführen.  

- **Python ToDo-App**  
  Kleine Flask-Anwendung mit SQLite als Beispielprojekt.  
  - Läuft intern als zwei Container (`ci-app-blue` und `ci-app-green`)  
  - Jenkins schaltet via Nginx zwischen beiden Versionen um → **Zero-Downtime-Deployment**  

- **Monitoring & Logging**  
  - `Prometheus` sammelt Metriken  
  - `Grafana` visualisiert Dashboards  
  - `cAdvisor` zeigt Container-Ressourcen  
  - `Dozzle` stellt Logs aller Container im Browser dar  

- **Security Scanning**  
  Jenkins-Pipelines führen mit **Trivy** Container- und Dependency-Scans durch, um bekannte Schwachstellen zu identifizieren.  

- **Einheitliche Umgebung**  
  Alles in `docker-compose.yml` definiert, mit persistenten Volumes für Jenkins, Grafana und Prometheus.  

- **UI-Komfort**  
  Deine ToDo-App enthält im Footer Links zu allen Services → kein Portsuchen mehr.  

---

## Installation & Setup

### Voraussetzungen

- [Git](https://git-scm.com/)  
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/) (ist bei Docker Desktop dabei)  

### Schritte

1. **Repository klonen**

```bash
git clone https://github.com/benedikt-wiesner-bl/ci-app.git
cd ci-app
```

2. **Services starten**

```bash
docker compose -f config/docker-compose.yml up --build -d
```

Das baut die Images und startet alle Services im Hintergrund.  
Beim ersten Start kann Jenkins ein paar Minuten brauchen.  

3. **Services im Browser aufrufen**

- **ToDo-App (immer via Nginx)** → [http://localhost:8085](http://localhost:8085)  
- **Jenkins** → [http://localhost:8080](http://localhost:8080)  
  - Initiales Admin-Password:  
    ```bash
    docker logs jenkins | grep "initialAdminPassword"
    ```
- **Grafana** → [http://localhost:3000](http://localhost:3000)  
  - Login: `admin` / `admin` (beim ersten Mal Passwort ändern)  
- **Prometheus** → [http://localhost:9090](http://localhost:9090)  
- **cAdvisor** → [http://localhost:8081](http://localhost:8081)  
- **Dozzle (Logs)** → [http://localhost:9999](http://localhost:9999)  

---

## CI/CD mit Blue-Green & Security Scan

Dein `Jenkinsfile` enthält mehrere Stages:  

1. **Build**  
   Baut die Python ToDo-App als Docker-Image.  

2. **Test**  
   Führt Unit-Tests (z. B. mit `pytest`) durch.  

3. **Security Scan (Trivy)**  
   Scannt das gebaute Docker-Image und deine Dependencies auf Schwachstellen.  

4. **Deploy (Blue-Green)**  
   - Jenkins deployt die neue Version in einen inaktiven Container (`blue` oder `green`).  
   - Führt einen Healthcheck (`/health`) durch.  
   - Schaltet Nginx auf die neue Version um → die alte Version bleibt für Rollback verfügbar.  

---

## Lokale Entwicklung der App

Die App ist für Docker gedacht, kann aber auch lokal laufen:

```bash
cd app
pip install -r requirements.txt
python __init__.py
```

→ dann läuft sie auf [http://localhost:5000](http://localhost:5000) (nur lokal, ohne Nginx).  

---

## Ordnerstruktur

```
ci-app/
│── app/                # Flask ToDo-App
│── infrastructure/      # Dockerfiles für Jenkins und App
│── grafana/             # Provisioning & Dashboards           
│── config/              # docker-compose.yml + nginx
│── prometheus.yml       # Prometheus-Konfiguration
│── README.md
```
