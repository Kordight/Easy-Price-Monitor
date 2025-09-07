from . import CORE_HANDLERS

def get_price(shop):
    handler = CORE_HANDLERS.get(shop["name"].lower())
    if not handler:
        raise NotImplementedError(f"Brak handlera dla sklepu {shop['name']}")
    return handler(shop["url"])
