import requests

BASE_URL = "http://127.0.0.1:8001"  # Replace with the correct base URL of your API

def test_create_sensor_valid():
    """Test adding a valid sensor through the API."""
    sensor_data = {
        "sensor_id": "sensor_integration_001",
        "sensor_type": "temperature",
        "location": "Integration Lab",
        "attributes": {"unit": "Celsius"}
    }

    response = requests.post(f"{BASE_URL}/sensors", json=sensor_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert "successfully" in response.json()["message"]


def test_create_sensor_duplicate():
    """Test adding a duplicate sensor through the API."""
    sensor_data = {
        "sensor_id": "sensor_integration_001",  # Use the same ID as the valid test
        "sensor_type": "temperature",
        "location": "Integration Lab",
        "attributes": {"unit": "Celsius"}
    }

    # Add the sensor for the first time
    requests.post(f"{BASE_URL}/sensors", json=sensor_data)

    # Try adding the same sensor again
    response = requests.post(f"{BASE_URL}/sensors", json=sensor_data)
    assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
    assert response.json()["detail"] == f"Sensor {sensor_data['sensor_id']} already exists."


def test_create_sensor_invalid():
    """Test adding a sensor with invalid data through the API."""
    sensor_data = {
        "sensor_id": "",
        "sensor_type": "",
        "location": "",
        "attributes": None
    }

    response = requests.post(f"{BASE_URL}/sensors", json=sensor_data)
    assert response.status_code == 422, f"Unexpected status code: {response.status_code}"