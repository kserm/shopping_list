FROM python:3.9-slim

WORKDIR /app

# Install only essential build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Create needed directories
RUN mkdir -p /app/database /app/app/static

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "2", "--timeout", "120", "run:app"]