# Use official slim Python runtime
FROM python:3.10-slim

# Prevent Python from writing .pyc files & enable unbuffered stdout
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies needed for C compilation and FAISS
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and frontend
COPY app ./app
COPY frontend ./frontend
COPY documents ./documents
COPY index.py .

# Expose FastAPI application port
EXPOSE 8000

# Entrypoint command to start FastAPI app with uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
