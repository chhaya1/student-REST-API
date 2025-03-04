# Use a slim Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install bash, netcat-openbsd (alternative to netcat), and iputils-ping (for ping)
RUN apt-get update && apt-get install -y bash netcat-openbsd iputils-ping

# Copy the requirements.txt file and install the Python dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Initialize migrations if the folder doesn't exist
RUN flask db init || true

RUN chmod +x app.sh
CMD ./app.sh
