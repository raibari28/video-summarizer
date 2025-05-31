FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file first (leverages Docker cache)
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the app port (Flask default or Railway uses $PORT)
EXPOSE 5000

# Set entrypoint for Railway compatibility (PORT env)
CMD ["python", "app.py"]
