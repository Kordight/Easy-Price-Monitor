from datetime import datetime, timedelta
import argparse
import random
from time import sleep

from pricephraser.core import get_price
from storage import STORAGE_HANDLERS, get_changes_mysql, get_all_product_ids
from visualization import PLOT_HANDLERS
from utils import load_products, load_app_config
from notifier import send_email_alert

PRODUCTS_FILE = "products.json"
DATABASE_CONFIG_FILE = "mysql_config.json"
DEFAULT_APP_CONFIG = "easyPrice_monitor_config.json"

settings = load_app_config(DEFAULT_APP_CONFIG)
interval = settings[0]["interval"][0] if settings[0].get("bUseDelayInterval") else None

def sleep_with_log(interval):
    """Ramdom sleep delay"""
    time_to_wait = random.randint(interval["minIntervalSeconds"], interval["maxInterval"])
    print(f"[{datetime.now()}] Waiting {time_to_wait}s until [{datetime.now() + timedelta(seconds=time_to_wait)}]")
    sleep(time_to_wait)


def main():
    parser = argparse.ArgumentParser(description="Easy Price Monitor")
    parser.add_argument("--handlers", nargs="+", help="List of handlers to run  (csv, mysql, default)")
    args = parser.parse_args()

    products = load_products(PRODUCTS_FILE)

    results = []

    for product in products:
        product_name = product["name"]
        print(f"\nProduct price monitoring: {product_name}\n")

        for shop in product["shops"]:
            try:
                price = get_price(shop)
                print(f"[{datetime.now()}] {shop['name']}: {price} PLN")
                results.append({
                    "product": product_name,
                    "shop": shop["name"],
                    "price": price,
                    "date": datetime.now().isoformat(),
                    "product_url": shop["url"]
                })
            except Exception as e:
                print(f"[{shop['name']}] Error: {e}")
            # Random delay between requests
            if interval:
                sleep_with_log(interval)

    # dynamic handlers execution
    if args.handlers:
        for handler_name in args.handlers:
            handler_name = handler_name.lower()
            if handler_name in STORAGE_HANDLERS:
                STORAGE_HANDLERS[handler_name](results)
            elif handler_name in PLOT_HANDLERS:
                PLOT_HANDLERS[handler_name](results)
            else:
                print(f"Invalid handler: {handler_name}")
    alerts_config = settings[0]["alerts"]
    if not alerts_config.get("bEnableAlerts", True):
        print("Alerts are disabled in config.")
        return
    percent_threshold = alerts_config["percentDropThreshold"]
    smtp_config = {
        "server": settings[0]["email"]["smtpServer"],
        "port": settings[0]["email"]["smtpPort"],
        "user": settings[0]["email"]["user"],
        "password": settings[0]["email"]["password"]
    }
    email_from = settings[0]["email"]["from"]
    email_to = settings[0]["email"]["to"]
    changes = []
    for handler_name in args.handlers or []:
        handler_name = handler_name.lower()
        if handler_name in STORAGE_HANDLERS:
            PRODUCT_IDS = []
            if handler_name == "mysql":
                PRODUCT_IDS = settings[0]["alerts"].get("ProductIDs", [])
                if not PRODUCT_IDS:
                    PRODUCT_IDS = get_all_product_ids()
                changes = get_changes_mysql(PRODUCT_IDS)
                print(f"Found {len(PRODUCT_IDS)} to alert")
            elif handler_name == "csv":
                print("CSV handler does not support alerts.")
        elif handler_name in PLOT_HANDLERS:
            PLOT_HANDLERS[handler_name](results)
        else:
            print(f"Invalid handler: {handler_name}")

    if changes:
        alerts = []
        for c in changes:
            percent = c.get("percent_change")
            if percent is not None:
                percent_float = float(percent)
                if abs(percent_float) >= percent_threshold:
                    print(f"[Price Change]: product_id={c['product_id']}, shop={c['shop_name']}, price={c['price']}, percent_change={percent_float}")
                    alerts.append(c)
        send_email_alert(alerts, smtp_config, email_from, email_to)
    else:
        print("No price changes detected.")



if __name__ == "__main__":
    main()
