FROM python:3.10-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (including bot folder)
COPY . .

# List files to verify (for debugging)
RUN ls -la /app/
RUN ls -la /app/bot/

# Run the bot
CMD ["python", "/app/bot/main.py"]
