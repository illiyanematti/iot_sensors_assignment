import requests

BASE_URL = "http://127.0.0.1:8001"

def test_get_sensors():
    """
    Test retrieving all sensors through the API.
    """
    response = requests.get(f"{BASE_URL}/sensors")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    data = response.json()
    assert "sensors" in data, "Response is missing the 'sensors' key."
    assert isinstance(data["sensors"], list), "'sensors' should be a list."
    assert len(data["sensors"]) > 0, "Expected at least one sensor in the response."