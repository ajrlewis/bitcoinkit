import datetime
import sys

from loguru import logger

from bitcoinkit.vendor.mempool import address, price
from bitcoinkit import utils


def aggregate(bitcoin_address: str, currency: str) -> dict:
    # Get all transaction details for a given Bitcoin address
    transactions = address.transaction_details(bitcoin_address)

    # Update the transactions with historical and current fiat values
    updated_transactions = []
    for transaction in transactions:
        logger.debug(f"{transaction = }")

        # Get conversion ratio from BTC to fiat at time of transaction
        fiat_to_btc = price.historical(
            timestamp=transaction["timestamp"], currency=currency
        )
        logger.debug(f"{fiat_to_btc = }")

        # Get conversion ratio from BTC to fiat now
        fiat_to_btc_now = price.current(currency=currency)
        logger.debug(f"{fiat_to_btc_now = }")

        # Convert satoshis into bitcoins
        value = utils.satoshis_to_bitcoins(transaction["value"])
        logger.debug(f"{value = }")
        value_fiat = fiat_to_btc * value
        logger.debug(f"{value_fiat = }")
        value_fiat_now = fiat_to_btc_now * value
        logger.debug(f"{value_fiat_now = }")

        # Compute the percentage gain
        value_fiat_gain = (value_fiat_now - value_fiat) / value_fiat * 100.0
        logger.debug(f"{value_fiat_gain = }")

        # Update transaction data
        updated_transaction = transaction.copy()
        updated_transaction[f"value_{currency.lower()}"] = value_fiat
        updated_transaction[f"value_{currency.lower()}_now"] = value_fiat_now
        updated_transaction[f"value_{currency.lower()}_gain"] = value_fiat_gain
        updated_transactions.append(updated_transaction)
        logger.debug(f"{updated_transaction = }")

    logger.debug(f"{updated_transactions = }")

    # Compute aggregate statistics
    number_of_transactions = len(updated_transactions)
    first_transaction_on = updated_transactions[-1]["timestamp"]
    last_transaction_on = updated_transactions[0]["timestamp"]
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    transaction_duration = datetime.datetime.strptime(
        last_transaction_on, timestamp_format
    ) - datetime.datetime.strptime(first_transaction_on, timestamp_format)
    transaction_duration = transaction_duration.days

    total_value = sum([t[f"value"] for t in updated_transactions])
    total_value = sum([t[f"value"] for t in updated_transactions])

    total_value = sum([t[f"value"] for t in updated_transactions])
    total_value_fiat = sum(
        [t[f"value_{currency.lower()}"] for t in updated_transactions]
    )
    total_value_fiat_now = sum(
        [t[f"value_{currency.lower()}_now"] for t in updated_transactions]
    )
    total_value_fiat_gain = (
        (total_value_fiat_now - total_value_fiat) / total_value_fiat * 100
    )
    total_value_fiat_cost_basis = total_value_fiat / utils.satoshis_to_bitcoins(
        total_value
    )

    aggregate = {
        "address": bitcoin_address,
        "number_of_transactions": number_of_transactions,
        "first_transaction_on": first_transaction_on,
        "last_transaction_on": last_transaction_on,
        "transaction_duration": f"{transaction_duration} days",
        "total_value": utils.to_string(total_value),
        "total_value_fiat": f"{total_value_fiat:,.2f} {currency}",
        "total_value_fiat_now": f"{total_value_fiat_now:,.2f} {currency}",
        "total_value_fiat_gain": f"{total_value_fiat_gain:,.2f}%",
        "total_value_fiat_cost_basis": f"{total_value_fiat_cost_basis:,.2f} {currency}",
    }
    logger.debug(f"{aggregate = }")
    return aggregate
