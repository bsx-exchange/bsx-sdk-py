.. _getting-started:

Getting started
===============

Introduction
------------

This SDK provide methods to perform basic trading operations on BSX Exchange

Basic usage
-----------
.. note::

    Remember to always keep your signer's private key securely stored and never expose it to the public.

Create the BSXInstance providing BSX Exchange domain, account and signer:

.. code-block:: python

    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment

    >>> wallet_private_key = "xxx"
    >>> signer_private_key = "yyy"
    >>> wallet = Account.from_key(wallet_private_key)
    >>> signer = Account.from_key(signer_private_key)
    >>> bsx_instance = BSXInstance(env=Environment.TESTNET, wallet=account, signer=signer)

Create an order
----------------

Create an order using `Create order API <https://api-docs.bsx.exchange/reference/orderservice_postorder>`_.

.. code-block:: python

    >>> import json
    >>> import dataclasses
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
    >>> print("Order: ", json.dumps(dataclasses.asdict(order)))

Cancel an order
----------------

Cancel an order using `Cancel an order API <https://api-docs.bsx.exchange/reference/cancelorder-1>`_.

.. code-block:: python

    >>> import json
    >>> import dataclasses

    >>> order_id = "xxx"
    >>> res = bsx_instance.cancel_order(order_id=order_id)
    >>> print("Order canceled.", json.dumps(dataclasses.asdict(res)))

Get open orders
-------------------

Get your open orders using `List all open orders API <https://api-docs.bsx.exchange/reference/getorders>`_.

.. code-block:: python

    >>> import json
    >>> import dataclasses

    >>> open_orders = bsx_instance.get_all_open_orders('BTC-PERP')
    >>> print("open orders: ", json.dumps(dataclasses.asdict(open_orders)))

