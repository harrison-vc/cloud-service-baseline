# Use an official Python runtime as a parent image
FROM python:3.11-slim as builder

# Set the working directory in the container
WORKDIR /app

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

# Create a non-root user for security
RUN groupadd -r serviceuser && useradd -r -g serviceuser serviceuser

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code
COPY app/ .

# Ensure the non-root user owns the app directory
RUN chown -R serviceuser:serviceuser /app

# Switch to the non-root user
USER serviceuser

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging_config.json"]
