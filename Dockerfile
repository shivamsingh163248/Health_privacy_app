# Use an official Python runtime
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 3000

# Run the Flask app
CMD ["python", "app.py"]
