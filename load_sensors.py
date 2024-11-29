import os
import csv
import requests

# Define the path to the sensor data CSV file
data_folder = os.path.join(os.path.dirname(__file__), 'data')
iot_sensors_file = os.path.join(data_folder, 'iot_sensors.csv')

# Define the API base URL
API_BASE_URL = "http://127.0.0.1:8001/sensors"

def load_sensors():
    """Load sensor data from CSV and send API requests to add sensors."""
    if not os.path.exists(iot_sensors_file):
        print(f"File not found: {iot_sensors_file}")
        return
    
    with open(iot_sensors_file, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Prepare sensor data
            sensor_data = {
                "sensor_id": row.get("device"),  # CSV column: device
                "sensor_type": row.get("sensor_type"),  # CSV column: sensor_type
                "location": row.get("location"),  # CSV column: location
                "attributes": eval(row.get("attributes", "{}"))  # CSV column: attributes (JSON-like string)
            }
            
            try:
                # Make the POST request to the API
                response = requests.post(API_BASE_URL, json=sensor_data)
                
                if response.status_code == 200:
                    print(f"Successfully added sensor: {sensor_data['sensor_id']}")
                else:
                    print(f"Failed to add sensor {sensor_data['sensor_id']}: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error adding sensor {sensor_data['sensor_id']}: {e}")

if __name__ == "__main__":
    load_sensors()