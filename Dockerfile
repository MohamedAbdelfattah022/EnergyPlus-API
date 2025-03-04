# Use an official Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Download and install EnergyPlus
RUN wget -O EnergyPlus.tar.gz https://github.com/NREL/EnergyPlus/releases/download/v24.2.0a/EnergyPlus-24.2.0-94a887817b-Linux-Ubuntu22.04-x86_64.tar.gz && \
    tar -xvzf EnergyPlus.tar.gz && \
    mv EnergyPlus-24.2.0-94a887817b-Linux-Ubuntu22.04-x86_64 /usr/local/EnergyPlus && \
    rm EnergyPlus.tar.gz

# Set environment variables for EnergyPlus
ENV PATH="/usr/local/EnergyPlus:${PATH}"
ENV ENERGYPLUS_DIR="/usr/local/EnergyPlus"

# Install Python dependencies
RUN pip3 install eppy flask pyngrok flask-cors python-dotenv gunicorn

# Create a directory for simulation output
RUN mkdir -p /content/simulation_output

# Copy the Python script and .env file into the container
COPY energyplus_api.py .env /app/

# Set the working directory
WORKDIR /app

# Expose the port for Flask
EXPOSE 8080

# Run the Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "energyplus_api:app"]