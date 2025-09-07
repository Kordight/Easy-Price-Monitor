import cloudscraper
from bs4 import BeautifulSoup

def get_price_xkom(url):
    """Downloads and parses the product page from X-Kom to extract the price."""
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    if response.status_code != 200:
        raise Exception(f"[xkom] Error, downloading webpage {url}: failed, response: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    whole = soup.select_one("span.parts__Price-sc-24f114ef-1")
    decimal = soup.select_one("span.parts__DecimalPrice-sc-24f114ef-4")
    if not whole or not decimal:
        raise Exception("[xkom] Price not found on the page")

    whole_text = whole.get_text(strip=True).replace(" ", "")
    decimal_text = decimal.get_text(strip=True).replace(" ", "").replace("zł", "")

    price = float(f"{whole_text}.{decimal_text}")
    return price
