# Use official Python image
FROM python:3.11-slim
FROM flask:2.3.2-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Set entrypoint for Flask
EXPOSE 8080
CMD ["python", "flask_app.py"]