-- Create the 'sensors' table
CREATE TABLE sensors (
    sensor_id VARCHAR(255) PRIMARY KEY,
    sensor_type VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    attributes JSONB
);

-- Create the 'readings' table
CREATE TABLE readings (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(255) NOT NULL REFERENCES sensors(sensor_id),
    timestamp TIMESTAMP NOT NULL,
    humidity DOUBLE PRECISION,
    light BOOLEAN,
    motion BOOLEAN,
    temperature DOUBLE PRECISION,
    is_anomalous BOOLEAN DEFAULT FALSE,
    anomaly_details JSONB DEFAULT NULL
);