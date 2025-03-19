# Use a lightweight Python image
FROM python:3.9-slim

# Create and use /app as the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose the port (Render will set $PORT at runtime)
EXPOSE 5000

# Start Gunicorn
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:$PORT", "--workers=1"]