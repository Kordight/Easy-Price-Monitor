import csv
from datetime import datetime

CSV_FILE = "price_history.csv"

def save_price_csv(results):
    """Saves price history to CSV file."""
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["product", "shop", "price", "date"])
        # add headers only if file is empty
        if f.tell() == 0:
            writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"[CSV] Saved {len(results)} records to: {CSV_FILE}")
