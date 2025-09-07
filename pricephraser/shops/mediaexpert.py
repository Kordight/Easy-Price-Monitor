import cloudscraper
from bs4 import BeautifulSoup
import json

def get_price_mediaexpert(url):
    """
    Pobiera cenę produktu ze strony Media Expert i zwraca ją jako float.
    """
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    if response.status_code != 200:
        raise Exception(f"Błąd pobierania strony {url}: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Zbierz wszystkie <script type="application/ld+json">
    scripts = soup.find_all("script", type="application/ld+json")
    if not scripts:
        raise Exception("Nie znaleziono żadnych danych JSON-LD na stronie")

    price = None

    for script in scripts:
        try:
            data = json.loads(script.string)
        except Exception:
            continue

        # Niektóre skrypty mają "@graph", więc trzeba przejść po elementach
        if isinstance(data, dict):
            # przypadek prosty
            if data.get("@type") == "Product" and "offers" in data:
                price = float(data["offers"]["price"])
                break
            # przypadek z @graph
            if "@graph" in data:
                for node in data["@graph"]:
                    if node.get("@type") == "Product" and "offers" in node:
                        price = float(node["offers"]["price"])
                        break

    if price is None:
        raise Exception("Nie udało się odczytać ceny z JSON-LD (Product)")

    return price
