# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script to the working directory
COPY sitemap_checker.py .

# Install the required Python packages
RUN pip install requests schedule

# Run the Python script when the container starts
CMD [ "python","-u","sitemap_checker.py" ]