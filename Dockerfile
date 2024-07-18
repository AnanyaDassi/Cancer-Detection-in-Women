# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
