from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.sensor import add_sensor, get_all_sensors  # Business logic for adding / fetching sensor

# Create a router instance
router = APIRouter()

# Define the request model for sensor metadata
class SensorRequest(BaseModel):
    sensor_id: str
    sensor_type: str
    location: str
    attributes: dict

@router.post("/sensors", tags=["Sensors"])
async def create_sensor(sensor: SensorRequest):
    """API endpoint to add a new sensor."""
    result, status_code = add_sensor(
        sensor_id=sensor.sensor_id,
        sensor_type=sensor.sensor_type,
        location=sensor.location,
        attributes=sensor.attributes
    )
    if status_code == 400:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/sensors")
async def get_sensors():
    """
    API endpoint to retrieve all sensors.
    """
    try:
        sensors = get_all_sensors()
        return {"sensors": sensors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sensors: {e}")