# Use the official lightweight Python image
FROM python:3.9-slim

# Set environment variables to avoid prompts during package installation
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Install necessary dependencies
RUN pip install --no-cache-dir Flask statsd

# Set the working directory in the container
WORKDIR /app

# Copy the app code into the container
COPY app.py /app

# Expose the port the app runs on
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

