import pandas as pd
import requests
import math

BASE_URL = "http://127.0.0.1:8001"
sensors_readings_file = "data/sensor_readings.csv"


def clean_value(value):
    """Replace NaN or None with null."""
    return None if (value is None or (isinstance(value, float) and math.isnan(value))) else value


def load_readings():
    """Load readings from CSV and send to API."""
    data = pd.read_csv(sensors_readings_file)

    for _, row in data.iterrows():
        reading_data = {
            "sensor_id": row["device"],
            "timestamp": row["timestamp"],
            "humidity": clean_value(row.get("humidity")),
            "light": clean_value(row.get("light")),
            "motion": clean_value(row.get("motion")),
            "temperature": clean_value(row.get("temperature")),
            "is_anomalous": clean_value(row.get("is_anomalous")),
            "anomaly_details": clean_value(None),  # Adjust if you have actual anomaly details
        }

        try:
            response = requests.post(f"{BASE_URL}/readings", json=reading_data)
            print(f"Response for {row['device']}: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Error sending reading for {row['device']}: {e}")


if __name__ == "__main__":
    load_readings()