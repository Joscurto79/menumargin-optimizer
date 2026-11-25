# Use official lightweight Python 3.12 Linux image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/
COPY run.py .

# Document that the container listens on port 5000
EXPOSE 5000

# Start the production Gunicorn WSGI server bound to all interfaces on port 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
