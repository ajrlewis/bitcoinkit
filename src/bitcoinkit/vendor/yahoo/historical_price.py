import datetime
import sys
from typing import Optional

from loguru import logger
import pandas as pd
import yahooquery as yq


intervals_to_days = {
    "1m": 1.0 / 60.0 / 24.0,
    "2m": 2.0 / 60.0 / 24.0,
    "5m": 5.0 / 60.0 / 24.0,
    "15m": 15.0 / 60.0 / 24.0,
    "30m": 30.0 / 60.0 / 24.0,
    "60m": 60.0 / 60.0 / 24.0,
    "90m": 90.0 / 60.0 / 24.0,
    "1h": 1.0 / 24.0,
    "1d": 1.0,
    "5d": 5.0,
    "1wk": 7.0,
    "1mo": 30.0,
    "3mo": 90.0,
}
currencies = ["USD", "GBP", "EUR"]
time_format = "%Y-%m-%d %H:%M:%S"


def historical_price(
    start: str, end: Optional[str] = None, interval: str = "1m", currency: str = "USD"
) -> Optional[float]:
    """ """
    if currency not in currencies:
        logger.error(f"currency must be one of {currencies}")
        return
    curreny = currency.upper()
    ticker = f"BTC-{currency}"
    logger.debug(f"{ticker = }")
    ticker_data = yq.Ticker([ticker], asynchronous=True)
    logger.debug(f"{ticker_data = }")

    if interval not in intervals_to_days.keys():
        logger.error(f"interval must be one of {intervals_to_days.keys()}")
        return

    start = datetime.datetime.strptime(start, time_format)
    logger.debug(f"{start = }")
    if not end:
        days = intervals_to_days[interval]
        end = start + datetime.timedelta(days=days)
        logger.debug(f"{end = }")
    else:
        end = datetime.datetime.strptime(end, time_format)
        logger.debug(f"{end = }")

    df = ticker_data.history(start=start, end=end, interval=interval)
    df = df.iloc[:-1].reset_index()  # don't include end row
    if df.empty:
        logger.error("no data frame returned from yahooquery")
        return
    logger.debug(f"{df = }")
    price = float(df.iloc[0]["open"])
    logger.debug(f"{price = }")
    return price
