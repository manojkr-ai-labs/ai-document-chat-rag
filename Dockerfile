# ============================================================
# Base image
# ============================================================
FROM python:3.12-slim

# ============================================================
# Environment variables
# ============================================================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Hugging Face cache
# Prevents HF from trying to write to /nonexistent
ENV HF_HOME=/app/.cache/huggingface
ENV HF_HUB_CACHE=/app/.cache/huggingface/hub

# ============================================================
# Working directory
# ============================================================
WORKDIR /app

# ============================================================
# System dependencies
# ============================================================
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# ============================================================
# Copy requirements
# ============================================================
COPY requirements.txt .

# ============================================================
# Upgrade pip
# ============================================================
RUN pip install --no-cache-dir --upgrade pip

# ============================================================
# Install CPU-only PyTorch
# ============================================================
RUN pip install --no-cache-dir \
    torch==2.13.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# ============================================================
# Install application dependencies
# ============================================================
RUN pip install --no-cache-dir -r requirements.txt

# ============================================================
# Copy application
# ============================================================
COPY . .

# ============================================================
# Create non-root user


RUN addgroup --system app \
    && adduser --system --ingroup app --home /app app \
    && mkdir -p /app/.cache/huggingface/hub /app/storage/sqlite /app/storage/chroma \
    && chown -R app:app /app

# ============================================================
# Run as non-root user
# ============================================================
USER app

# ============================================================
# Expose application port
# ============================================================
EXPOSE 8000

# ============================================================
# Health check
# ============================================================
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=30s \
    --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# ============================================================
# Start application
# ============================================================
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn src.api.app:app --host 0.0.0.0 --port 8000"]