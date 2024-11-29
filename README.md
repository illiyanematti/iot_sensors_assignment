# **Smart Home IoT Sensor Data Management System**

## **Overview**

This project is a Python-based application for managing IoT sensor data in a smart home system. The system combines structured and unstructured data storage:

1. **PostgreSQL Database**:

   - Stores sensor metadata and readings.
   - Includes a `JSONB` field for flexible storage of anomaly details.

2. **Unstructured JSON File**:
   - Logs anomalies in an `anomalies.json` file for additional redundancy and non-relational use cases.

This architecture offers a scalable, flexible, and efficient solution for managing IoT sensor data.

---

## **Features**

- **Sensor Management**: Add, retrieve, and manage IoT sensors.
- **Reading Management**: Add sensor readings and associate them with metadata.
- **Anomaly Detection**: Identify and log anomalies in both structured and unstructured formats.
- **Validation**: Ensure unique sensor IDs and validate data integrity.
- **API Integration**: RESTful APIs for managing sensors, readings, and anomalies.

---

## **Data Model**

### **1. Sensors Table**

| **Column**    | **Type**       | **Description**                                       |
| ------------- | -------------- | ----------------------------------------------------- |
| `sensor_id`   | `VARCHAR(255)` | Unique identifier for each sensor.                    |
| `sensor_type` | `VARCHAR(50)`  | Type of sensor (e.g., temperature, humidity, motion). |
| `location`    | `VARCHAR(100)` | Physical location of the sensor.                      |
| `attributes`  | `JSONB`        | Additional metadata (e.g., `{"unit": "Celsius"}`).    |

### **2. Readings Table**

| **Column**        | **Type**           | **Description**                                                                 |
| ----------------- | ------------------ | ------------------------------------------------------------------------------- |
| `id`              | `SERIAL`           | Unique identifier for each reading.                                             |
| `sensor_id`       | `VARCHAR(255)`     | Foreign key referencing the `sensor_id` in the `sensors` table.                 |
| `timestamp`       | `TIMESTAMP`        | Timestamp when the reading was recorded.                                        |
| `humidity`        | `DOUBLE PRECISION` | Humidity reading as a percentage (RH).                                          |
| `light`           | `BOOLEAN`          | Boolean indicating whether light is detected.                                   |
| `motion`          | `BOOLEAN`          | Boolean indicating whether motion is detected.                                  |
| `temperature`     | `DOUBLE PRECISION` | Temperature reading in °C.                                                      |
| `is_anomalous`    | `BOOLEAN`          | Flag indicating whether the reading is an anomaly.                              |
| `anomaly_details` | `JSONB`            | JSONB column for storing details of the anomaly (e.g., type, reason, severity). |

### **3. Unstructured Data (Anomalies JSON File)**

The `anomalies.json` file stores an array of anomalies in JSON format. Each entry includes:

- `sensor_id`: Identifier for the sensor.
- `timestamp`: Time of the anomaly.
- `details`: JSON object describing the anomaly.

**Example `anomalies.json`**:

```json
[
  {
    "sensor_id": "b8:27:eb:bf:9d:51",
    "timestamp": "2023-11-29T14:05:00",
    "details": {
      "type": "temperature",
      "reason": "Temperature below 0°C",
      "severity": "critical"
    }
  }
]
```

## Setup Instruction

1. Prerequisites
   • Python 3.10+
   • PostgreSQL (v15)

2. Clone the Repository
   git clone https://github.com/illiyanematti/iot_sensors_assignment.git
   cd iot_sensors_assignment

3. Set Up the Virtual Environment
   python3 -m venv iot_project_env
   source iot_project_env/bin/activate
   pip install -r requirements.txt

4. Configure the Database

   1. Create the database:
      createdb -U iotuser iot_sensors_project

   2. Apply the schema:
      psql -U iotuser -d iot_sensors_project -f database/schema.sql

5. Run the Application  
   uvicorn api.main_api:app --reload --port 8001
   • Access the API documentation:
   • Swagger UI: http://127.0.0.1:8001/docs
   • Redoc: http://127.0.0.1:8001/redoc

## API Documentation

1.  POST /sensors
    Add a new sensor.
    • Request:
    {
    "sensor_id": "sensor_001",
    "sensor_type": "temperature",
    "location": "Living Room",
    "attributes": {"unit": "Celsius"}
    }

• Response:
{"message": "Sensor sensor_001 added successfully"}

2. GET /sensors
   Retrieve all sensors.
   • Response:
   {
   "sensors": [
   {"sensor_id": "sensor_001", "sensor_type": "temperature", "location": "Living Room", "attributes": {"unit": "Celsius"}}
   ]
   }

## Testing

Run tests using pytest:
pytest test/
