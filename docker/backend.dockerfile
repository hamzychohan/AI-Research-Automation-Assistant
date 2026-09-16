FROM python:3.11-slim

WORKDIR /workspace

# Install system-level build tools and PostgreSQL clients
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies first for efficient cache layers usage
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source tree
COPY backend/ /workspace/

# Expose API service port
EXPOSE 8000

# Automatically run Alembic migrations on task boot-up before launching Uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
