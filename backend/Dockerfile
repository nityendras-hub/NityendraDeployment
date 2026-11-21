# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install standard compiler dependencies if needed and the Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the serialized model and application script into the container
COPY superkart_model.joblib .
COPY app.py .

# Expose port 7860 for the Flask app
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Define the command to run the application using python directly
CMD ["python", "app.py"]
