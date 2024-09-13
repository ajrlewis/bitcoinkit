import re

from loguru import logger

satoshis_per_bitcoin = 100_000_000
millisatoshis_per_satoshi = 1_000


def bitcoins_to_satoshis(bitcoins: float) -> int:
    return int(bitcoins * satoshis_per_bitcoin)


def satoshis_to_bitcoins(satoshis: int) -> float:
    return satoshis / satoshis_per_bitcoin


def satoshis_to_millisatoshis(satoshis: int) -> int:
    return satoshis * millisatoshis_per_satoshi


def millisatoshis_to_satoshis(millisatoshis: int) -> int:
    return millisatoshis / millisatoshis_per_satoshi


def to_string(satoshis: int) -> str:
    sats_str = f"{int(satoshis)}"
    n_digits = len(sats_str)
    if n_digits < 8:
        padding = "0" * (8 - n_digits)
        sats_str = f"{padding}{sats_str}"
    btc_str = sats_str[:-8] or "0"
    btc_str = f"{int(btc_str):,}"
    sats_str = f"{sats_str[-8:-6]} {sats_str[-6:-3]} {sats_str[-3:]}"
    sats_str = f"{btc_str}.{sats_str} BTC"
    return sats_str


def from_string(sats_str: str) -> int:
    satoshis = re.sub("[^0-9]", "", sats_str)
    logger.debug(f"{satoshis = }")
    return int(satoshis)


def main():
    value = 215780
    satoshis_string = to_string(value)
    logger.debug(f"{satoshis_string = }")
    satoshis = from_string(satoshis_string)
    logger.debug(f"{satoshis = }")


if __name__ == "__main__":
    main()
