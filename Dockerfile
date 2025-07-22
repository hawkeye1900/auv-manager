# Use official Python 3 image as a base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app

# Set the environment variable for Flask to know the entry point
ENV FLASK_APP=run.py

# Expose port 5000 (default Flask port)
EXPOSE 5000

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

RUN apt-get update && apt-get install -y postgresql-client

