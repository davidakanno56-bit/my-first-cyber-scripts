# Use an official lightweight Python runtime
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for Scapy packet capturing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    scapy \
    reportlab \
    requests

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Command to run the API server when container starts
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]