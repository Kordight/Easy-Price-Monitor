from datetime import datetime
import argparse

from pricephraser.core import get_price
from storage import STORAGE_HANDLERS
from visualization import PLOT_HANDLERS
from utils import load_products

PRODUCTS_FILE = "products.json"
DATABASE_CONFIG_FILE = "mysql_config.json"

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
                    "date": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"[{shop['name']}] Błąd: {e}")

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


if __name__ == "__main__":
    main()
