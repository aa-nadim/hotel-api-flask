# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ../../requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . .

# Expose the port the service will run on
EXPOSE 5002

# Command to run the application
CMD ["python3", "app.py"]
