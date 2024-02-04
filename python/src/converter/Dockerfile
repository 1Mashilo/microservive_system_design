FROM python:3.12-slim-bullseye

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        build-essential ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy the application code into the container
COPY . /app

# Expose port 5000 to the outside world
EXPOSE 000

# Command to run the application
CMD ["python3", "consumer.py"]
