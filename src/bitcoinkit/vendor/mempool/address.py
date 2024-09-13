import datetime
import sys
import time
from typing import Optional

from loguru import logger
import requests

base_url = "https://mempool.space/api/address/{address}"


def chain_stats(address: str) -> Optional[dict]:
    """Returns the Mempool chain statistics for a given address."""
    logger.debug(f"{address = }")

    # Don't overload the API
    time.sleep(0.5)

    url = base_url.format(address=address)
    logger.debug(f"{url = }")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"{data = }")
    except requests.exceptions.HTTPError as e:
        message = f"unable to query address: {e = }"
        logger.error(message)
        return
    try:
        chain_stats = data["chain_stats"]
    except KeyError as e:
        message = f"unable to get chain_stats: {e =}"
        logger.error(message)
        return
    else:
        return chain_stats


def transactions(address: str) -> Optional[list[dict]]:
    """Returns concise details of a given transaction."""

    # Don't overload the API
    time.sleep(0.5)

    url = f"{base_url.format(address=address)}/txs"
    logger.debug(f"{url = }")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"unable to grab transactions: {e = }")
    else:
        data = response.json()
        logger.debug(f"{data = }")
        return data


def transaction_detail(tx: dict) -> dict:
    """Returns concise details of a given transaction."""
    txid = tx["txid"]
    value = int(tx["vout"][0]["value"])
    block_height = int(tx["status"]["block_height"])
    block_time = int(tx["status"]["block_time"])
    timestamp = f"{datetime.datetime.utcfromtimestamp(block_time)}"
    detail = {
        "txid": txid,
        "value": value,
        "timestamp": timestamp,
        "block_height": block_height,
        "block_time": block_time,
    }
    return detail


def transaction_details(address: str) -> Optional[list[dict]]:
    data = transactions(address)
    details = []
    for tx in data:
        detail = transaction_detail(tx)
        logger.debug(f"{detail = }")
        details.append(detail)
    logger.debug(f"{details = }")
    return details
