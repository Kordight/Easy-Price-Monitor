import json
import os

DEFAULT_PRODUCTS = {
    "products": [
        {
            "id": 1,
            "name": "ASRock X870 Pro RS",
            "shops": [
                {
                    "name": "x-kom",
                    "url": "https://www.x-kom.pl/p/1281720-plyta-glowna-socket-am5-asrock-x870-pro-rs.html"
                }
            ]
        },
        {
            "id": 2,
            "name": "Gembird CR2032 (2szt)",
            "shops": [
                {
                    "name": "x-kom",
                    "url": "https://www.x-kom.pl/p/748392-bateria-i-akumulatorek-gembird-cr2032-2szt.html?cid=api09&eid=pdp_pcacc"
                }
            ]
        }
    ]
}

def load_products(PRODUCTS_FILE):
    """Load products from JSON file, if not create default file"""
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_PRODUCTS, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Created default product list: {PRODUCTS_FILE}")

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["products"]

DEFAULT_MYSQL_CONFIG = {
    "connection": {
        "host": "localhost",
        "database": "easy_price_monitor",
        "user": "easy-price-monitor",
        "password": "",
        "port": 3306,
    }
}


def load_mysql_config(MYSQL_CONFIG):
    """Load MySQL config from JSON file, if not create default file"""
    if not os.path.exists(MYSQL_CONFIG):
        with open(MYSQL_CONFIG, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_MYSQL_CONFIG, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Created default mySQL config file: {MYSQL_CONFIG}")
        return DEFAULT_MYSQL_CONFIG["connection"]

    with open(MYSQL_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config["connection"]

DEFAULT_APP_CONFIG = {
    "settings": [
        {
            "bUseDelayInterval": True,
            "interval": [
                {
                    "minIntervalSeconds": 5,
                    "maxInterval": 20
                }
            ]
        }
    ]
}


def load_app_config(APP_CONFIG):
    """Load app config from JSON file, if not create default file"""
    if not os.path.exists(APP_CONFIG):
        with open(APP_CONFIG, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_APP_CONFIG, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Utworzono domyślny plik {APP_CONFIG}")
        return DEFAULT_APP_CONFIG["settings"]

    with open(APP_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config["settings"]