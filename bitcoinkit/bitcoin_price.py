import requests

VALID_CURRENCIES = ["USD", "GBP", "EUR"]
COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency}"
)


def _check_currency_is_valid(currency):
    if currency not in VALID_CURRENCIES:
        raise ValueError(
            f"Invalid currency: {currency}. Valid currencies are: {', '.join(VALID_CURRENCIES)}"
        )


def _get_price_from_coingecko(currency):
    _check_currency_is_valid(currency)
    url = COINGECKO_URL.format(currency=currency.lower())
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["bitcoin"][currency.lower()]
    else:
        raise requests.exceptions.RequestException(
            "Failed to fetch Bitcoin price from CoinGecko"
        )


def _get_price(currency):
    return _get_price_from_coingecko(currency)


def gbp():
    return _get_price("GBP")


def eur():
    return _get_price("EUR")


def usd():
    return _get_price("USD")


def main():
    price_usd = usd()
    price_gbp = gbp()
    price_eur = eur()
    print(f"Bitcoin price in USD: {price_usd:,}")
    print(f"Bitcoin price in GBP: {price_gbp:,}")
    print(f"Bitcoin price in EUR: {price_eur:,}")


if __name__ == "__main__":
    main()
