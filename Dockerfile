# Use a slim Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cloud Run listens on PORT env var (default 8080)
ENV PORT=8080

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Run with uvicorn (Cloud Run expects 0.0.0.0 and PORT)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]