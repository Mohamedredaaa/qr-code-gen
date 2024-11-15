# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for pycairo and other libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libgirepository1.0-dev \
    pkg-config \
    python3-dev \
    libffi-dev \
    && apt-get clean

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
