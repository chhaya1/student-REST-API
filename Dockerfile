# Use official Python base image
FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
