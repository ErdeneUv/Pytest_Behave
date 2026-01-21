import logging
import os
import mysql.connector
from tests.steps.build_link_api import logger

env = os.getenv("ENVIRONMENT")
def get_db_conn():
    db_config = {
        'host': os.getenv(f'{env}_db_host'),
        'port': os.getenv(f'{env}_db_port'),
        #'name': os.getenv(f'{env}_db_name'),
        'user': os.getenv(f'{env}_db_user'),
        'password': os.getenv(f'{env}_db_pass'),
    }
    conn = mysql.connector.connect(**db_config)

    logger=logging.getLogger()
    logger.info('DB connection is established\n')
    return conn


def close_db_conn(cursor=None, conn=None):
    try:
        if cursor:
            cursor.close()
    except Exception as e:
        print(f"Error closing cursor: {e}")
    try:
        if conn:
            conn.close()
            logger.info('DB connection is closed\n')
    except Exception as e:
        print(f"Error closing connection: {e}")