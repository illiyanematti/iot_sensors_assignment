import pandas as pd
import requests
import json
import os

BASE_URL = "http://127.0.0.1:8001"
sensor_anomalies_file = "data/sensor_anomalies.csv"
anomalies_json_path = "database/anomalies.json"


def log_to_json(sensor_id, timestamp, anomaly_details):
    """Log anomaly details to the JSON file with validation."""
    anomaly_entry = {
        "sensor_id": sensor_id,
        "timestamp": timestamp,
        "anomaly_details": anomaly_details
    }

    # Load existing anomalies from JSON file
    if os.path.exists(anomalies_json_path):
        with open(anomalies_json_path, 'r') as file:
            anomalies = json.load(file)
    else:
        anomalies = []

    # Check for duplicates
    if anomaly_entry not in anomalies:
        anomalies.append(anomaly_entry)
        with open(anomalies_json_path, 'w') as file:
            json.dump(anomalies, file, indent=4)
        print(f"Anomaly for {sensor_id} logged in JSON file.")
    else:
        print(f"Duplicate anomaly for {sensor_id}. Skipping addition to JSON file.")


def load_anomalies():
    """Load anomalies from CSV and send to API."""
    data = pd.read_csv(sensor_anomalies_file)

    for _, row in data.iterrows():
        anomaly_details = {
            "reason": row["reason"],
            "severity": row["severity"]
        }
        anomaly_data = {
            "sensor_id": row["device"],
            "timestamp": row["timestamp"],
            "is_anomalous": True,
            "anomaly_details": anomaly_details
        }

        # Send anomaly to the API
        response = requests.post(f"{BASE_URL}/readings", json=anomaly_data)
        if response.status_code == 200:
            print(f"Response for {row['device']}: {response.status_code} - {response.json()}")

            # Log to JSON file
            log_to_json(row["device"], row["timestamp"], anomaly_details)
        else:
            print(f"Error adding anomaly for {row['device']}: {response.status_code} - {response.text}")


if __name__ == "__main__":
    load_anomalies()