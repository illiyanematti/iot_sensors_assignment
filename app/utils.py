import csv

def log_unprocessed_readings_to_csv(readings, file_path):
    """Log unprocessed readings to a CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=readings[0].keys())
        writer.writeheader()
        writer.writerows(readings)
    print(f"Logged {len(readings)} unprocessed readings to {file_path}.")