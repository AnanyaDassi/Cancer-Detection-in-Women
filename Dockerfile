# Use the base image created earlier
FROM ml-base

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 80
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
