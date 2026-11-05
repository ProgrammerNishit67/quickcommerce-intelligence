FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and seed data
COPY backend/ ./backend/
COPY data/ ./data/
COPY sql_queries/ ./sql_queries/

WORKDIR /app/backend

# Seed database and start uvicorn
CMD ["sh", "-c", "python app/services/seed_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
