FROM python:3.10-slim

# Install ffmpeg and build tools needed for Python dependencies
RUN apt-get update \
    && apt-get install -y ffmpeg build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

ENV PORT 7860
CMD gunicorn app:app --bind 0.0.0.0:$PORT --timeout 600
