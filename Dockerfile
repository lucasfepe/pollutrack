# Use the official Python 3.10 image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install required system dependencies (like GCC for building)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install fastapi \
    uvicorn \
    opentelemetry-sdk \
    opentelemetry-api \
    opentelemetry-instrumentation-fastapi \
    opentelemetry-exporter-otlp-proto-http \
    -r requirements.txt

# Copy your application code into the container
COPY . .

# Expose the port your app will run on
EXPOSE 8000

# OpenTelemetry settings for FastAPI
ENV OTEL_SERVICE_NAME=my-fastapi-app
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://datadog-agent:4318
ENV OTEL_TRACES_SAMPLER=always_on
ENV OTEL_METRICS_EXPORTER=none

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
