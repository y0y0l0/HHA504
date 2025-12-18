# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files (main.py, index.html, Procfile, data/, reports/)
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set environment variable for Cloud Run
ENV PORT=8080

# Run Flask app with gunicorn (as per Procfile)
CMD exec gunicorn -b 0.0.0.0:8080 main:app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]