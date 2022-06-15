import pyodbc
from loggers import logger
import time
import requests
import json
import datetime
import os 

from main import update_sales_orders

WORKING_DIR = "C:\goprime\sync_service"
config = None 
with open (os.path.join(WORKING_DIR, "test_config.json"), "r") as f:
    config = json.load(f)

HEADERS = {
    "Authorization": config.get('token'),
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def to_dict(row):
    return dict(zip([t[0] for t in row.cursor_description], row))


def main():
    logger.info("Connecting to database")
    conn = pyodbc.connect(
        "Driver=ODBC Driver 11 for SQL Server;"
        f"Server={config.get('server')};"
        f"Database={config.get('database')};"
        f"user={config.get('user')};"
        f"password={config.get('password')};"
        "Trusted_Connection=yes;"
    )

    update_sales_orders(conn, config, HEADERS)

if __name__ == "__main__":
    main()