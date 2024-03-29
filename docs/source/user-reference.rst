User reference
==============

Core client
-----------
BSXInstance provides methods to interact with BSX Exchange and abstract away the complication of message signing,
authentication, and session management

BSXInstance can be initialized either with an API key or the main wallet's private key.

- **Create BSXInstance using private key:**

.. code-block:: python
    
    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment
    >>> wallet_private_key = "xxx"
    >>> signer_private_key = "yyy"
    >>> wallet = Account.from_key(wallet_private_key)
    >>> signer = Account.from_key(signer_private_key)
    >>> bsx_instance = BSXInstance(env=Environment.TESTNET, wallet=account, signer=signer)

- **Create BSXInstance using API key:**

.. code-block:: python

    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment
    >>> signer_private_key = "yyy"
    >>> signer = Account.from_key(signer_private_key)
    >>> bsx_instance = BSXInstance.from_api_key(api_key="xxx", api_secret="zzz", signer=signer, env=Environment.TESTNET)

Below are supported APIs to interact with BSX Exchange

- **Create an order:**

.. code-block:: python

    >>> import time
    >>> from decimal import Decimal
    >>> from bsx_py.common.types.market import CreateOrderParams, Side
    >>> params = CreateOrderParams(
        side=Side.BUY,
        product_index=3,
        price=Decimal('100.3'),
        size=Decimal('0.1'),
        time_inf_force="GTC",
        nonce=int(time.time_ns())
    )
    >>> order = bsx_instance.create_order(params=params)

- **Cancel an order:**

.. code-block:: python

    >>> res = bsx_instance.cancel_order(order_id="xxx")

- **Cancel multiple orders:**

.. code-block:: python

    >>> res = bsx_instance.cancel_bulk_orders(order_ids=["xxx", "yyy"])

- **Cancel all open orders:**

.. code-block:: python

    >>> res = bsx_instance.cancel_all_orders(product_id="BTC-PERP")

- **Get all open orders:**

.. code-block:: python

    >>> res = bsx_instance.get_all_open_orders(product_id="BTC-PERP")

- **Get order history:**

.. code-block:: python

    >>> params = GetOrderHistoryParams(
        product_id="SOL-PERP",
        start_time=datetime.now() - timedelta(days=30),
        end_time=datetime.now(),
        limit=100,
        statuses=[OrderStatus.DONE, OrderStatus.OPEN, OrderStatus.PENDING],
    )
    >>> history = instance.get_order_history(params)

- **Submit withdrawal request:**

.. code-block:: python

    >>> params = WithdrawParams(
        amount=Decimal("10"),
        nonce=int(time.time_ns())
    )
    >>> is_success = instance.submit_withdrawal_request(params)

- **Get portfolio detail:**

.. code-block:: python

    >>> portfolio = instance.get_portfolio_detail(params)

