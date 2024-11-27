import datetime
import sys
import time
from typing import Optional

from loguru import logger
import numpy as np
import pandas as pd
import requests

base_url = "https://mempool.space/api/v1/blocks/"


def get_latest_block_data():
    block_data = {}
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"unable to get response: {e = }")
        return block_data
    data = response.json()
    if data and len(data) > 1:
        data = data[0]  # latest block
        # logger.debug(f"{data = }")
        block_data = {}
        block_data["block_id"] = data.get("id")
        block_data["block_height"] = data.get("height")
        block_data["block_timestamp"] = data.get("timestamp")
        block_data["block_nonce"] = data.get("nonce")
        block_data["block_difficulty"] = data.get("difficulty")
        block_data["block_tx_count"] = data.get("tx_count")
        block_data["block_mediantime"] = data.get("mediantime")
        # logger.debug(f"{block_data = }")
        return block_data
