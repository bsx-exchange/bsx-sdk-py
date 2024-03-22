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

wallet_private_key = "xxx"
signer_private_key = "yyy"
wallet = Account.from_key(wallet_private_key)
signer = Account.from_key(signer_private_key)
```

### Create the BSXInstance providing BSX Exchange domain, account and signer:

```python
from bsx_py import BSXInstance, Environment

bsx_instance = BSXInstance(env=Environment.TESTNET, wallet=wallet, signer=signer)
```

### Perform basic operations:

```python
# Placing orders
from bsx_py.common.types.market import CreateOrderParams

params = CreateOrderParams(
    side=Side.BUY,
    product_index=3,
    price=price,
    size=size,
    time_in_force="GTC",
    nonce=int(time.time())
)
order = bsx_instance.create_order(params)
print("order id:", order.id)
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
