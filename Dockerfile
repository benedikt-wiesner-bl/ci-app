FROM python:3.11-slim

WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Damit "import app" funktioniert
ENV PYTHONPATH=/app

EXPOSE 5000
CMD ["python", "-m", "app"]
