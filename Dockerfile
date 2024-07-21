# Dockerfile
FROM python:3.11-slim

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 80
EXPOSE 8000


# Command to run the application
CMD ["uvicorn", "API.main:app", "--host", "0.0.0.0", "--port", "8000"]
