# Base image: Alpine with Python
FROM python:3.9-alpine

# Install socat
RUN apk add --no-cache socat

# Set working directory
WORKDIR /app

# Copy all challenge files
COPY . /app

# Install Python requirements (if any)
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the main script is executable
RUN chmod +x malboot_nc.py

# Expose the port for netcat users
EXPOSE 1337

# Start socat to forward TCP connections to the Python script
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 malboot_nc.py",pty,stderr
