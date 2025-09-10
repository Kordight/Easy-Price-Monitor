from .shops import xkom
from .shops import mediaexpert

CORE_HANDLERS = {
    "x-kom": xkom.get_price_xkom,
    "mediaexpert": mediaexpert.get_price_mediaexpert,
    # Can add more shops here
}
