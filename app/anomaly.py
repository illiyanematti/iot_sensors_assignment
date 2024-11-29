import json
from datetime import datetime

def detect_anomalies(sensor_data):
    anomalies = []

    if sensor_data['temperature'] < 0:
        anomalies.append({
            "sensor_id": sensor_data['sensor_id'],
            "timestamp": str(datetime.now()),
            "type": "temperature",
            "reason": "Temperature below 0°C",
            "severity": "critical"
        })
    if sensor_data['humidity'] is None:
        anomalies.append({
            "sensor_id": sensor_data['sensor_id'],
            "timestamp": str(datetime.now()),
            "type": "humidity",
            "reason": "Humidity reading missing",
            "severity": "warning"
        })

    # Append anomalies to a JSON file
    with open('anomalies.json', 'a') as f:
        for anomaly in anomalies:
            json.dump(anomaly, f)
            f.write('\n')

    return anomalies