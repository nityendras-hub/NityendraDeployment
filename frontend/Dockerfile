# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install the Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend application code
COPY app_frontend.py .

# Expose port 8501 for the Streamlit dashboard
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the Streamlit application
CMD ["streamlit", "run", "app_frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
