import pyodbc
from loggers import logger
import time
import requests
import json
import datetime
import os 

WORKING_DIR = "C:\goprime\sync_service"
config = None 
with open (os.path.join(WORKING_DIR, "test_config.json"), "r") as f:
    config = json.load(f)

print(config.get("token"))
HEADERS = {
    "Authorization": config.get('token'),
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def to_dict(row):
    return dict(zip([t[0] for t in row.cursor_description], row))

def update_sales_orders(conn):
    resp = requests.get(
        f"http://{config.get('host')}/api/method/"
        "alpha_packaging.alpha_packaging.public_api.query_existing_orders", 
        headers=HEADERS
    )
    logger.info(resp.content)
    cursor = conn.cursor()
    existing_orders = resp.json().get("message", [])
    diff_list = []
    for order in existing_orders:
        cursor.execute("""
            SELECT [OrderNum] as sales_order_no
                ,[ExtOrderNum] as purchase_order_no
                ,[OrderDate] as sales_order_date
                ,[Code] as item_code
                ,[QtyOutstanding] as quantity 
                ,[Account] as customer_number
                ,[Name] as customer_name
                ,[Description_1] 
                ,[fUnitPriceIncl]
                ,[fUnitPriceExcl]
                ,[dTimeStamp] as timestamp
            FROM [Alpha Packaging].[dbo].[_bvSalesOrdersFull]
            WHERE OrderNum = '{}' AND Code = '{}'
            AND DocumentStateDesc not in ( 'Archived', 'Quote', 'Cancelled', 'Template')
        """.format(order.get('sales_order_no'), order.get('item_code')))
        
        values = [to_dict(r) for r in cursor]
        if values:
            fields = values[0]
            diff = {'sales_order_no': order.get('sales_order_no')}
            for k,v in order.items():
                if k in ["timestamp", "sales_order_date"]: continue
                if fields.get(k) is not None and fields.get(k) != v:
                    value = fields[k]
                    if isinstance(value, datetime.datetime):
                        value = value.strftime("%Y-%m-%dT%H:%M%S.000Z")
                    diff[k] = value

            if len(diff) > 1:
                logger.info(f"Diffs found for {order.get('sales_order_no')}")
                diff_list.append(diff)

    if len(diff_list) > 0:
        logger.info("Sending diffs to server.")
        logger.info(f"diffs: {json.dumps(diff_list)}")
        resp = requests.get(
            f"http://{config.get('host')}/api/method/"
            "alpha_packaging.alpha_packaging.public_api.sync_existing_orders", 
            headers=HEADERS,
            json={'diffs': json.dumps(diff_list)}
        )
        logger.info(resp.content)


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

    update_sales_orders(conn)

if __name__ == "__main__":
    main()