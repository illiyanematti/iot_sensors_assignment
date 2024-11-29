import psycopg2
from psycopg2 import sql
import json

# Load database configurations from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

def connect_to_db():
    connection = psycopg2.connect(
        dbname=config['database']['dbname'],
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host'],
        port=config['database']['port']
    )
    return connection