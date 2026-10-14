# Dockerfile for Flask backend
FROM python:3.10-slim
WORKDIR /app
# Install system dependencies (if any) and python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy application code
COPY . ./
# Expose Flask port (default from config)
EXPOSE 5000
# Use gunicorn for production (optional) – here we use python directly for simplicity
CMD ["python", "app.py"]
