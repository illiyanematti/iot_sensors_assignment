import sys
import os
import json
import pandas as pd
import datetime

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db_connection import connect_to_db
from app.sensor import add_sensor
from app.reading import add_reading

# Define file paths
data_folder = os.path.join(os.path.dirname(__file__), 'Data')
anomalies_json_path = os.path.join('database', 'anomalies.json')

# Error log for tracking issues
error_log = []

def log_error(message):
    """Log error messages with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    error_log.append(formatted_message)
    print(formatted_message)

def save_error_log():
    """Save error logs to a file."""
    if error_log:
        log_file_path = "error_log.txt"
        with open(log_file_path, "a") as log_file:
            for message in error_log:
                log_file.write(message + "\n")
        print(f"Error log saved to {log_file_path}.")

def initialize_database():
    """Ensure the database is initialized with the correct schema."""
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Create tables if they don't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            sensor_id VARCHAR(255) PRIMARY KEY,
            sensor_type VARCHAR(50),
            location VARCHAR(100),
            attributes JSONB
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id SERIAL PRIMARY KEY,
            sensor_id VARCHAR(255) REFERENCES sensors(sensor_id),
            timestamp TIMESTAMP,
            humidity DOUBLE PRECISION,
            light BOOLEAN,
            motion BOOLEAN,
            temperature DOUBLE PRECISION,
            is_anomalous BOOLEAN DEFAULT FALSE,
            anomaly_details JSONB
        );
        """)
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully!")
    except Exception as e:
        log_error(f"Critical error initializing database: {e}")
        raise SystemExit("Database initialization failed. Exiting...")

def initialize_unstructured_database():
    """Ensure the anomalies JSON file exists."""
    if not os.path.exists(anomalies_json_path):
        with open(anomalies_json_path, 'w') as file:
            json.dump([], file)
    print("Unstructured database initialized successfully!")

def validate_sensor(sensor_id, sensor_type, location, attributes):
    """Validate sensor metadata."""
    if not isinstance(sensor_id, str) or not sensor_id:
        raise ValueError(f"Invalid sensor_id: {sensor_id}")
    if not isinstance(sensor_type, str) or not sensor_type:
        raise ValueError(f"Invalid sensor_type: {sensor_type}")
    if not isinstance(location, str) or not location:
        raise ValueError(f"Invalid location: {location}")
    if not isinstance(attributes, dict):
        raise ValueError(f"Invalid attributes: {attributes}")

def validate_timestamp(timestamp):
    """Validate timestamp format."""
    try:
        pd.to_datetime(timestamp)
    except Exception as e:
        raise ValueError(f"Invalid timestamp: {timestamp}. Error: {e}")

def main():
    """Main entry point for the app."""
    initialize_database()
    initialize_unstructured_database()
    save_error_log()

if __name__ == "__main__":
    main()