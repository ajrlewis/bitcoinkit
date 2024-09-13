# BitcoinKit

![My Project Logo](images/logo.png)

A collection of bitcoin utility methods.

## Installation

Install via pip:

```bash
pip install git+https://github.com/ajrlewis/bitcoinkit.git
```

## Examples

1. Compute statistics on the transactions associated to a given bitcoin address:

```python
from bitcoinkit import statistics
from loguru import logger

bitcoin_address = "<Your Bitcoin Address>"
currency = "USD"
aggregate = statistics.aggregate(bitcoin_address, currency)
logger.info(f"{aggregate = }")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
