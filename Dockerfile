# Use official Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

# Set working directory
WORKDIR $APP_HOME

# Copy project files to the container
COPY . $APP_HOME

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8001

# Command to run the application
CMD ["uvicorn", "api.main_api:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]