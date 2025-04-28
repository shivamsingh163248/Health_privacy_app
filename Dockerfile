# Use an official Python runtime
FROM python:3.9-slim

# Add metadata label
LABEL org.opencontainers.image.source="https://github.com/shivamsingh163248/Health_privacy_app"

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 3000
EXPOSE 3000

# Run the Flask app
CMD ["python", "app.py"]
