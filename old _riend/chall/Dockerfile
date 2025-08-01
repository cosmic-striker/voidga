# Use the official Python image based on Alpine Linux
FROM python:alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY HAND_GAME.py .

# Install socat using the Alpine package manager
RUN apk add --no-cache socat

# Expose the port that socat will listen on
EXPOSE 2006

# Use socat to execute the Python script for each incoming connection
CMD ["socat", "TCP-LISTEN:2006,reuseaddr,fork", "EXEC:python -u HAND_GAME.py"]