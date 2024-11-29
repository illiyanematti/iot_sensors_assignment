import sys
import os
import pytest

# Dynamically add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# In main.py
from api.routes.sensor_routes import router as sensor_router
from app.db_connection import connect_to_db

def test_db_connection():
    """Test the database connection."""
    try:
        connection = connect_to_db()
        assert connection is not None, "Failed to establish a database connection."
        connection.close()
        print("Database connection successful!")
    except Exception as e:
        pytest.fail(f"Database connection test failed: {e}")
        
if __name__ == "__main__":
    test_db_connection()