FROM python:3.9-slim

WORKDIR /app

# Create database directory
RUN mkdir -p /app/database

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Use environment variable for port
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${APP_PORT:-5000} run:app"]