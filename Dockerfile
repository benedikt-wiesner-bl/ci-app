FROM python:3.11-slim

WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Damit "import app" funktioniert
ENV PYTHONPATH=/app
ENV FLASK_APP=app

RUN mkdir -p /app/data
EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

