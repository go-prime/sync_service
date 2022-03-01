import pyodbc
from loggers import logger
import time
import requests

logger.info("running service")
HEADERS = {
    "Authorization": "token 4ab84db48b15118:8cca3b8064037ae",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
def main():
    '''
    use pyodbc.drivers() to get the driver list.
    Get server name from the properties of the database server.
    validate database name
    '''
    
    logger.info("Connecting to database")
    # conn = pyodbc.connect(
    #     "Driver=ODBC Driver 17 for SQL Server;"
    #     "Server=DESKTOP-U6DOJ9D;"
    #     "Database=bench;"
    #     "Trusted_Connection=yes;"
    # )
    # cursor = conn.cursor()
    # logger.info("Successfully connected.")
    # cursor.execute("select customer from bench.dbo.invoices")
    # # data = list(cursor)
    # for i in data:
    #     logger.info(str(i))

    resp = requests.get(
        "http://167.99.205.84:81/api/method/"
        "alpha_packaging.alpha_packaging.public_api.last_order", 
        headers=HEADERS
    )
    logger.info(resp.content)
    latest = resp.json().get("latest")
    if latest:
        # only get latest items
        logger.info(f"Collecting data since {latest}")
    else:
        # initial fetch of data 
        logger.info("Collecting all orders")

    resp = requests.get(
        "http://167.99.205.84:81/api/method/"
        "alpha_packaging.alpha_packaging.public_api.sync_orderbook", 
        headers=HEADERS, 
        data={"orders": []}
    )
    if resp.status_code == 200:
        logger.info("Successfully synced orderbook")
    else:
        logger.error("Failed to sync order book.")
    logger.info(resp.content)

main()

# if __name__ == "__main__":
#     main()