# Use a lightweight Python base
FROM python:3.9-slim

# Install system tools (FFmpeg) needed for audio
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set up the app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Open the port for the web
EXPOSE 10000

# Start the server with a 2-MINUTE TIMEOUT (Fixes the crash)
CMD ["gunicorn", "-b", "0.0.0.0:10000", "--timeout", "120", "app:app"]
