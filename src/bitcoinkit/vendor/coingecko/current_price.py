from typing import Optional

from loguru import logger
import requests

currencies = ["USD", "GBP", "EUR"]
base_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency}&include_market_cap=true"


def current_price(currency: str) -> Optional[float]:
    if currency.upper() not in currencies:
        logger.error(f"currency must be one of {currencies}")
        return
    else:
        currency = currency.lower()
        logger.debug(f"{currency = }")

    url = base_url.format(currency=currency)
    logger.debug(f"{url = }")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"{e = }")
        return

    try:
        data = response.json()
        logger.debug(f"{data = }")
        bitcoin_price = data["bitcoin"][currency]
    except KeyError as e:
        logger.error(f"{e = }")
        return
    else:
        return bitcoin_price
