# Use the official Python base image from Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory (where the Dockerfile is) to /app in the container
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit will use
EXPOSE 8501

# Command to run Streamlit app
CMD ["streamlit", "run", "src/app.py"]
