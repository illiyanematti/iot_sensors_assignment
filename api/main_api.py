from fastapi import FastAPI
from api.routes.sensor_routes import router as sensor_router

app = FastAPI()

# Include the routers
app.include_router(sensor_router)
