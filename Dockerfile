# Use a slim Python image for production
FROM python:3.9-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libcairo2-dev \
    libpango1.0-dev \
    libjpeg-dev \
    zlib1g-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    libpangocairo-1.0-0 \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Use Gunicorn as the WSGI server for production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
