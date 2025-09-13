from . import CORE_HANDLERS

def get_price(shop):
    handler = CORE_HANDLERS.get(shop["name"].lower())
    if not handler:
        raise NotImplementedError(f"No handler for {shop['name']} found.")
    return handler(shop["url"])
