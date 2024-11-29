import uvicorn
from api.main_api import app

if __name__ == "__main__":
    # Start the FastAPI server
    uvicorn.run(app, host="127.0.0.1", port=8001)