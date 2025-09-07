import cloudscraper
from bs4 import BeautifulSoup

def get_price_xkom(url):
    """
    Pobiera cenę produktu ze strony x-kom i zwraca ją jako float.
    """
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    if response.status_code != 200:
        raise Exception(f"Błąd pobierania strony {url}: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    whole = soup.select_one("span.parts__Price-sc-24f114ef-1")
    decimal = soup.select_one("span.parts__DecimalPrice-sc-24f114ef-4")
    if not whole or not decimal:
        raise Exception("Nie znaleziono elementów ceny na stronie")

    price = float(f"{whole.get_text(strip=True)}.{decimal.get_text(strip=True).replace('zł','')}")
    return price
