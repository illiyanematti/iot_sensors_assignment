import json
from app.db_connection import connect_to_db


def sensor_exists(sensor_id: str) -> bool:
    """
    Check if a sensor exists in the database.

    Args:
        sensor_id (str): The ID of the sensor to check.

    Returns:
        bool: True if the sensor exists, False otherwise.
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM sensors WHERE sensor_id = %s", (sensor_id,))
        count = cursor.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"Error checking sensor existence: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
        

def add_sensor(sensor_id: str, sensor_type: str, location: str, attributes: dict):
    connection = None
    cursor = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Check if the sensor already exists
        cursor.execute("SELECT COUNT(*) FROM sensors WHERE sensor_id = %s", (sensor_id,))
        if cursor.fetchone()[0] > 0:
            return {"error": f"Sensor {sensor_id} already exists."}, 400  # Add status code here

        # Insert the new sensor
        cursor.execute("""
            INSERT INTO sensors (sensor_id, sensor_type, location, attributes)
            VALUES (%s, %s, %s, %s)
        """, (sensor_id, sensor_type, location, json.dumps(attributes)))
        connection.commit()
        return {"message": f"Sensor {sensor_id} added successfully."}, 201  # Add status code here
    except Exception as e:
        return {"error": f"Error adding sensor: {e}"}, 500  # Add status code here
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        
def get_all_sensors():
    """Retrieve all sensors from the database."""
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT sensor_id, sensor_type, location, attributes FROM sensors")
        sensors = cursor.fetchall()
        return [
            {
                "sensor_id": sensor[0],
                "sensor_type": sensor[1],
                "location": sensor[2],
                "attributes": sensor[3],
            }
            for sensor in sensors
        ]
    except Exception as e:
        print(f"Error retrieving sensors: {e}")
        return {"error": f"Error retrieving sensors: {e}"}
    finally:
        cursor.close()
        connection.close()