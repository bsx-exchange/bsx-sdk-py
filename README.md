# BSX Exchange Python SDK

This is the Python SDK for the [BSX Exchange API](https://api-docs.bsx.exchange/reference/general-information).

See [SDK docs](https://bsx-engineering.github.io) to get started.

## Requirements

- Python 3.9 or above

## Installation

You can install the SDK via pip:

```bash
pip install bsx-sdk-py
```

## Basic usage

### Create a wallet and a signer from private keys

```python
from eth_account import Account

wallet_private_key = "0x0000000000000000000000000000000000000000000000000000000000000000"
signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
wallet = Account.from_key(wallet_private_key)
signer = Account.from_key(signer_private_key)
```

### Create the BSXInstance using the main wallet's private key:

```python
from eth_account import Account
from bsx_py import BSXInstance, Environment

wallet_private_key = "0x0000000000000000000000000000000000000000000000000000000000000000"
signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
wallet = Account.from_key(wallet_private_key)
signer = Account.from_key(signer_private_key)
bsx_instance = BSXInstance(env=Environment.TESTNET, wallet=wallet, signer=signer)
```

### Create the BSXInstance using an active API key:

```python
from eth_account import Account
from bsx_py import BSXInstance, Environment

signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
signer = Account.from_key(signer_private_key)
bsx_instance = BSXInstance.from_api_key(api_key="xxx", api_secret="zzz", signer=signer, env=Environment.TESTNET)
```

### Perform basic operations:

```python
# Placing orders
import time
from decimal import Decimal
from bsx_py.common.types.market import CreateOrderParams, Side, OrderType

params = CreateOrderParams(
    type=OrderType.LIMIT,
    side=Side.BUY,
    product_index=3,
    price=Decimal("100"),
    size=Decimal("1"),
    time_in_force="GTC",
    nonce=int(time.time())
)
order = bsx_instance.create_order(params)
print(order)
```

See [Getting Started](https://bsx-engineering.github.io/getting-started.html) for more.

## Running locally

1. Clone [github repo](https://github.com/bsx-engineering/bsx-python-sdk)

2. Install poetry

```

$ curl -sSL https://install.python-poetry.org | python3 -

```

3. Setup a virtual environment and activate it

```

$ python3 -m venv venv
$ source ./venv/bin/activate

```

4. Install dependencies via `poetry install`
