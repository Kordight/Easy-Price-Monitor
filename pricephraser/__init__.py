from .shops import xkom

CORE_HANDLERS = {
    "x-kom": xkom.get_price_xkom,
    # można dodawać kolejne sklepy
}
