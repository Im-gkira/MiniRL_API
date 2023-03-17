# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

COPY ./requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# Run the command to start the Flask app
CMD ["/bin/bash", "docker-entrypoint.sh"]
