# Dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire api folder to the container
COPY . .

# Env variables for the API
ENV API_PORT=8000

# By default, let's run the training script
CMD ["python", "inference_api.py"]