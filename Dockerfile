# Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Create app directory
WORKDIR /app

# Copy the main application to the container
COPY ./API /app/API

# Copy requirements.txt to the container
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 80
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "API.main:app", "--host", "0.0.0.0", "--port", "80"]
