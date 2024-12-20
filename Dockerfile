# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set environment variables to avoid python buffering output
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the dependencies first to leverage Docker caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "app.py"]