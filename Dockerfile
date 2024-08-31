# Use the official Python image as the base image
FROM python:3.10-slim
MAINTAINER Konstantin Verner <konst.verner@gmail.com>

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and other necessary files
COPY pyproject.toml .
COPY src ./src
COPY tests ./tests

# Copy the .env file into the container
COPY .env /app/

# Install build dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install project dependencies
RUN pip install --no-cache-dir .

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1

# Expose port (if needed, adjust according to your application needs)
EXPOSE 8000

# Define the command to run the application
CMD ["python", "src/llm_chatbot_api/api/main.py"]
