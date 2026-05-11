FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements_complete.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements_complete.txt

# Copy application files
COPY main_backend_v3.py .
COPY utils_v2.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main_backend_v3.py"]
