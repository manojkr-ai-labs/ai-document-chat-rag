# Base image
FROM python:3.12-slim

# Prevent Python from buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker layer caching)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]