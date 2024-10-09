import datetime
import sys
import time
from typing import Optional

from loguru import logger
import numpy as np
import pandas as pd
import requests


base_url = "https://mempool.space/api/v1/historical-price"
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


def historical(
    timestamp: Optional[str] = None, currency: str = "USD"
) -> Optional[pd.DataFrame]:
    """Returns the historical fiat price of 1 BTC as a data frame."""

    # Don't overload the API
    time.sleep(0.5)

    # Ensure the currency is valid
    currency = currency.upper()
    if currency not in currencies:
        logger.error(f"currency must be one of {currencies}")
        return
    logger.debug(f"{currency = }")

    # Ensure the timestamp is correctly formatted then convert it a Unix timestamp
    if timestamp is not None:
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

    # Create GET request parameters
    params = {"currency": currency}
    if timestamp is not None:  # Missing timestamp will default to entire history
        params["timestamp"] = timestamp
    logger.debug(f"{params = }")

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"unable to get response: {e = }")
        return

    try:
        data = response.json()
        # logger.debug(f"{data = }")
        prices = data["prices"]
        logger.debug(f"{len(prices) = }")
        df = pd.DataFrame(prices)
        logger.debug(f"{df = }")
    except Exception as e:
        message = f"something went wrong: {e = }"
        logger.error(message)
    else:
        return df


def main():
    # timestamp = "2021-04-19 10:07:10"
    timestamp = None
    currency = "USD"
    df = historical(timestamp=timestamp, currency=currency)
    print()
    print(df)


if __name__ == "__main__":
    main()
