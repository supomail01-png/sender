FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main_backend_v3.py .

# Expose port (Railway will override this)
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "uvicorn main_backend_v3:app --host 0.0.0.0 --port ${PORT:-8000}"]
