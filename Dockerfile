FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Run the bot directly (not as module)
CMD ["python", "bot/main.py"]
