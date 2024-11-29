from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.sensor import add_sensor  # Business logic for adding sensor

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
