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

Create the BSXInstance using main wallet's private key:

.. code-block:: python

    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment

    >>> wallet_private_key = "0x0000000000000000000000000000000000000000000000000000000000000000"
    >>> signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
    >>> wallet = Account.from_key(wallet_private_key)
    >>> signer = Account.from_key(signer_private_key)
    >>> bsx_instance = BSXInstance(env=Environment.TESTNET, wallet=account, signer=signer)

Create the BSXInstance using an active API key:

.. code-block:: python

    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment

    >>> signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
    >>> signer = Account.from_key(signer_private_key)
    >>> bsx_instance = BSXInstance.from_api_key(api_key="xxx", api_secret="zzz", signer=signer, env=Environment.TESTNET)

Create the BSXInstance for a smart contract wallet:

.. code-block:: python

    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment

    >>> contract_address = "0x2222222222222222222222222222222222222222"
    >>> signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
    >>> signer = Account.from_key(signer_private_key)
    >>> signature = "0xd0704e0f838435aca87ed544bffcff596878275f22cbb7e6b26d782a72db3085562f2817068f71128a7278510de29763279cd71f6b08684e8fb420acc410ef6820d243daa5fbb2dfef1c3bc8a7e00e749cf8ff228f6d7ace881c9bf78bac9026b3126bd44e3c5086939031c45fb6d72639877bfec1ed8223195ef0426b3da51a4f20000000000000000000000000F6CDA5B4432D66267941bA9eb1Bd3E285B3aE13e00000000000000000000000000000000000000000000000000000000000000c3000000000000000000000000000000000000000000000000000000000000000082d0704e0f838435aca87ed544bffcff596878275f22cbb7e6b26d782a72db3085562f2817068f71128a7278510de29763279cd71f6b08684e8fb420acc410ef6820d243daa5fbb2dfef1c3bc8a7e00e749cf8ff228f6d7ace881c9bf78bac9026b3126bd44e3c5086939031c45fb6d72639877bfec1ed8223195ef0426b3da51a4f20"
    >>> nonce = 1722488593775000001
    >>> bsx_instance = BSXInstance.from_smart_contract(
            env=Environment.TESTNET, contract_address=contract_address,
            signature=signature, nonce=nonce, signer=signer
        )

.. note::

    Please read this `doc <https://api-docs.bsx.exchange/reference/sign-messages>`_ for how to generate the signature.
    You can use `gen_register_typed_message_for_smart_contract <api-reference.html#bsx_py.typed_message.gen_register_typed_message_for_smart_contract>`_ function to get the typed message for signing.

Create an order
----------------

Create an order using `Create order API <https://api-docs.bsx.exchange/reference/orderservice_postorder>`_.

.. code-block:: python

    >>> import time
    >>> from decimal import Decimal
    >>> from bsx_py.common.types.market import CreateOrderParams, Side, OrderType

    >>> params = CreateOrderParams(
        type=OrderType.LIMIT,
        side=Side.BUY,
        product_index=3,
        price=Decimal('100.3'),
        size=Decimal('0.1'),
        time_inf_force='GTC',
        nonce=int(time.time_ns()),
        post_only=false,
        client_order_id='522005f7bfdb48c98b931a40296cdf96'
    )
    >>> order = bsx_instance.create_order(params=params)
    >>> print("Order: ", order)

Cancel an order
----------------

Cancel an order using `Cancel an order API <https://api-docs.bsx.exchange/reference/cancelorder-1>`_.

.. code-block:: python

    >>> order_id = "xxx"
    >>> res = bsx_instance.cancel_order(order_id=order_id)
    >>> print("Order canceled. ", res)

Get open orders
-------------------

Get your open orders using `List all open orders API <https://api-docs.bsx.exchange/reference/getorders>`_.

.. code-block:: python

    >>> open_orders = bsx_instance.get_all_open_orders('BTC-PERP')
    >>> print("open orders: ", open_orders)

