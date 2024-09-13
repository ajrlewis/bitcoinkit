import datetime
import sys
import time
from typing import Optional

from loguru import logger
import requests

base_url = "https://mempool.space/api/v1/historical-price?currency={currency}&timestamp={timestamp}"
currencies = ["USD", "EUR", "GBP", "CAD", "CHF", "AUD", "JPY"]

timestamp_format = "%Y-%m-%d %H:%M:%S"


def current(currency: str = "USD"):
    # Get the current Unix timestamp
    now = time.time()
    logger.debug(f"{now = }")
    # Convert to required format
    timestamp = datetime.datetime.utcfromtimestamp(now).strftime(timestamp_format)
    logger.debug(f"{timestamp = }")
    # Get the price at the current time
    price = historical(timestamp, currency=currency)
    logger.debug(f"{price = }")
    return price


def historical(timestamp: str, currency: str = "USD") -> Optional[float]:
    """Returns the historical fiat price  of 1 BTC."""

    # Don't overload the API
    time.sleep(0.5)

    # Ensure the currency is valid
    currency = currency.upper()
    if currency not in currencies:
        logger.error(f"currency must be one of {currencies}")
        return
    logger.debug(f"{currency = }")

    # Ensure the timestamp is correctly formatted then convert it a Unix timestamp
    try:
        timestamp = datetime.datetime.strptime(timestamp, timestamp_format)
        logger.debug(f"{timestamp = }")
    except ValueError as e:
        logger.error(
            f"timestamp should be a string of the form, e.g. 2008-10-31 00:00:00: {e = }"
        )
        return
    try:
        timestamp = timestamp.timestamp()
        timestamp = int(timestamp)
        logger.debug(f"{timestamp = }")
    except ValueError as e:
        logger.error(f"unable to extract timestamp and cast to int: {e = }")
        return

    url = base_url.format(currency=currency, timestamp=int(timestamp))
    logger.debug(f"{url = }")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"unable to get response: {e = }")
        return

    try:
        data = response.json()
        logger.debug(f"{data = }")
        prices = data["prices"]
        logger.debug(f"{prices = }")
        price = prices[0][currency]
        logger.debug(f"{price = }")
    except Exception as e:
        message = f"something went wrong: {e = }"
        logger.error(message)
    else:
        return price
