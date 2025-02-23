# Build Stage
FROM python:3.10-alpine AS builder

# Install build dependencies including libpq-dev and postgresql-client
RUN apk update && apk add --no-cache build-base gcc musl-dev libpq-dev postgresql-client

WORKDIR /app

# Copy requirements to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run Stage (Final Image)
FROM python:3.10-alpine

WORKDIR /app

# Install libpq-dev and postgresql-client for psycopg2
RUN apk add --no-cache libpq-dev postgresql-client

# Copy dependencies and app code from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
