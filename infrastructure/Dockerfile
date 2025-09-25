FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --upgrade setuptools==78.1.1

COPY . .

ENV PYTHONPATH=/app
ENV FLASK_APP=app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
