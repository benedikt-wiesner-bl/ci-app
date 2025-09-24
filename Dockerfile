FROM python:3.11-slim

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code
COPY . .

# Damit "import app" funktioniert
ENV PYTHONPATH=/app
ENV FLASK_APP=app

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
