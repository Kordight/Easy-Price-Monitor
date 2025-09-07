import mysql.connector
from mysql.connector import Error
from datetime import datetime

def ensure_tables_exist(cursor):
    """Tworzy brakujące tabele products, shops i prices."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shops (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            url_pattern TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            shop_id INT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            currency VARCHAR(10) DEFAULT 'PLN',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (shop_id) REFERENCES shops(id)
        )
    """)

def save_price_mysql(results, db_config):
    """Zapisuje wyniki do tabel products/shops/prices w MySQL."""
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 🔍 Sprawdź czy istnieją wszystkie tabele
        ensure_tables_exist(cursor)

        for row in results:
            product_name = row["product"]
            shop_name = row["shop"]
            price = row["price"]
            timestamp = row.get("date", datetime.now())
            currency = row.get("currency", "PLN")

            # 1. Produkt
            cursor.execute("SELECT id FROM products WHERE name = %s", (product_name,))
            product = cursor.fetchone()
            if not product:
                cursor.execute("INSERT INTO products (name) VALUES (%s)", (product_name,))
                conn.commit()
                product_id = cursor.lastrowid
            else:
                product_id = product[0]

            # 2. Sklep
            cursor.execute("SELECT id FROM shops WHERE name = %s", (shop_name,))
            shop = cursor.fetchone()
            if not shop:
                cursor.execute("INSERT INTO shops (name) VALUES (%s)", (shop_name,))
                conn.commit()
                shop_id = cursor.lastrowid
            else:
                shop_id = shop[0]

            # 3. Cena
            cursor.execute("""
                INSERT INTO prices (product_id, shop_id, price, currency, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """, (product_id, shop_id, price, currency, timestamp))

        conn.commit()
        print(f"[MySQL] Zapisano {len(results)} rekordów do tabeli 'prices'")

    except mysql.connector.Error as e:
        print(f"[MySQL] Błąd: {e}")
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()
