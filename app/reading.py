import json
from datetime import datetime
from app.db_connection import connect_to_db
from app.sensor import sensor_exists


def add_reading(sensor_id, timestamp, humidity=None, light=None, motion=None, temperature=None, is_anomalous=False, anomaly_details=None):
    """
    Add a new reading to the database.

    Args:
        sensor_id (str): ID of the sensor.
        timestamp (str): Timestamp in 'YYYY-MM-DD HH:MM:SS' format.
        humidity (float, optional): Humidity value. Defaults to None.
        light (bool, optional): Light detection status. Defaults to None.
        motion (bool, optional): Motion detection status. Defaults to None.
        temperature (float, optional): Temperature value. Defaults to None.
        is_anomalous (bool, optional): Whether the reading is anomalous. Defaults to False.
        anomaly_details (dict, optional): Additional details about the anomaly. Defaults to None.
    """
    
    if not sensor_exists(sensor_id):
        message = f"Sensor {sensor_id} does not exist"
        print(message)
        return {"message": message}
    
    try:
        # Validate the timestamp
        try:
            parsed_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return {"message": f"Invalid timestamp format: {timestamp}. Expected 'YYYY-MM-DD HH:MM:SS'."}

        # Check if the sensor exists
        if not sensor_exists(sensor_id):
            return {"message": f"Sensor {sensor_id} does not exist. Reading not added."}

        # Serialize anomaly details to JSON, if provided
        anomaly_details_json = json.dumps(anomaly_details) if anomaly_details else None

        # Database connection
        connection = connect_to_db()
        cursor = connection.cursor()

        # Insert reading into the database
        cursor.execute("""
            INSERT INTO readings (sensor_id, timestamp, humidity, light, motion, temperature, is_anomalous, anomaly_details)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (sensor_id, parsed_timestamp, humidity, light, motion, temperature, is_anomalous, anomaly_details_json))

        connection.commit()
        return {"message": f"Reading for sensor {sensor_id} added successfully."}
    except Exception as e:
        return {"message": f"Error adding reading: {e}"}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()