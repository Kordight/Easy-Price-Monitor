from . import csv_storage
from . import mysql_storage
from utils import load_mysql_config

def mysql_handler(results):
    db_config = load_mysql_config("mysql_config.json")
    mysql_storage.save_price_mysql(results, db_config)

STORAGE_HANDLERS = {
    "csv": csv_storage.save_price_csv,
    "mysql": mysql_handler
}
