# Dockerfile for slim test
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt 

# Copy the entire project
COPY . .

# Set environment variables for the test
ENV API_HOST="localhost"
ENV API_PORT=8000

# By default, let's run the training script
CMD ["python3", "test_inference_api.py"]