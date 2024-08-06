User reference
==============

Core client
-----------
BSXInstance provides methods to interact with BSX Exchange and abstract away the complication of message signing,
authentication, and session management

For normal wallets, BSXInstance can be initialized either with an API key or the main wallet's private key.

- **Create BSXInstance using private key:**

.. code-block:: python
    
    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment
    >>> wallet_private_key = "0x0000000000000000000000000000000000000000000000000000000000000000"
    >>> signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
    >>> wallet = Account.from_key(wallet_private_key)
    >>> signer = Account.from_key(signer_private_key)
    >>> bsx_instance = BSXInstance(env=Environment.TESTNET, wallet=account, signer=signer)

- **Create BSXInstance using API key:**

.. code-block:: python

    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment
    >>> signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
    >>> signer = Account.from_key(signer_private_key)
    >>> bsx_instance = BSXInstance.from_api_key(api_key="xxx", api_secret="zzz", signer=signer, env=Environment.TESTNET)

If you are using a multisig wallet, you can create a BSXInstance using this code below

.. code-block:: python

    >>> from eth_account import Account
    >>> from bsx_py import BSXInstance, Environment

    >>> wallet_address = "0x2222222222222222222222222222222222222222"
    >>> signer_private_key = "0x1111111111111111111111111111111111111111111111111111111111111111"
    >>> signer = Account.from_key(signer_private_key)
    >>> signature = "0xd0704e0f838435aca87ed544bffcff596878275f22cbb7e6b26d782a72db3085562f2817068f71128a7278510de29763279cd71f6b08684e8fb420acc410ef6820d243daa5fbb2dfef1c3bc8a7e00e749cf8ff228f6d7ace881c9bf78bac9026b3126bd44e3c5086939031c45fb6d72639877bfec1ed8223195ef0426b3da51a4f20000000000000000000000000F6CDA5B4432D66267941bA9eb1Bd3E285B3aE13e00000000000000000000000000000000000000000000000000000000000000c3000000000000000000000000000000000000000000000000000000000000000082d0704e0f838435aca87ed544bffcff596878275f22cbb7e6b26d782a72db3085562f2817068f71128a7278510de29763279cd71f6b08684e8fb420acc410ef6820d243daa5fbb2dfef1c3bc8a7e00e749cf8ff228f6d7ace881c9bf78bac9026b3126bd44e3c5086939031c45fb6d72639877bfec1ed8223195ef0426b3da51a4f20"
    >>> nonce = 1722488593775000001
    >>> bsx_instance = BSXInstance.from_multi_sig_wallet(
            env=Environment.TESTNET, wallet_address=wallet_address,
            signature=signature, nonce=nonce, signer=signer
        )

.. note::

    Please read this `doc <https://api-docs.bsx.exchange/reference/sign-messages>`_ for how to generate the signature.
    You can use `gen_register_typed_message_for_multisig_wallet <api-reference.html#bsx_py.typed_message.gen_register_typed_message_for_multisig_wallet>`_ function to get the typed message for signing.
APIs
------------
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

- **Update orders in batch:**

.. code-block:: python

    >>> from bsx_py.common.types.market import *
    >>> params = BatchOrderUpdateParams(operations=[
        CreateOrderParams(
            type=OrderType.LIMIT,
            side=Side.BUY,
            product_index=3,
            price=Decimal('100.3'),
            size=Decimal('0.1'),
            time_inf_force='GTC',
            nonce=int(time.time_ns()),
            post_only=false,
            client_order_id='522005f7bfdb48c98b931a40296cdf96'
        ),
        CancelOrderParams(order_id="8a325a62-80f0-46ef-8943-3267b381271f"),
        CancelAllParams(product_id="SOL-PERP"),
        CancelOrdersParams(order_ids=['8a325a62-80f0-46ef-8943-3267b381271f'])
    ])
    >>> res = bsx_instance.batch_update_orders(params)

- **Get all open orders:**

.. code-block:: python

    >>> res = bsx_instance.get_all_open_orders(product_id="BTC-PERP")

- **Get order history:**

.. code-block:: python

    >>> from bsx_py.common.types.market import *
    >>> params = GetOrderHistoryParams(
        product_id="SOL-PERP",
        start_time=datetime.now() - timedelta(days=30),
        end_time=datetime.now(),
        limit=100,
        statuses=[OrderStatus.DONE, OrderStatus.OPEN, OrderStatus.PENDING],
        client_order_id=["abc", "xyz"]
    )
    >>> history = bsx_instance.get_order_history(params)

- **Submit withdrawal request:**

.. code-block:: python

    >>> from bsx_py.common.types.account import *
    >>> params = WithdrawParams(
        amount=Decimal("10"),
        nonce=int(time.time_ns())
    )
    >>> is_success = bsx_instance.submit_withdrawal_request(params)

- **Get portfolio detail:**

.. code-block:: python

    >>> portfolio = bsx_instance.get_portfolio_detail()

- **Get trade history:**

.. code-block:: python

    >>> from bsx_py.common.types.market import *
    >>> history = bsx_instance.get_user_trade_history(params=GetTradeHistoryParams(
        product_id='BTC-PERP',
        start_time=datetime.now() - timedelta(days=1),
        end_time=datetime.now(),
        page=1,
        limit=50
    ))

- **Get funding rate history:**

.. code-block:: python

    >>> from bsx_py.common.types.market import *
    >>> history = bsx_instance.get_funding_history(params=GetFundingHistoryParams(
        product_id='BTC-PERP',
        start_time=datetime.now() - timedelta(days=1),
        end_time=datetime.now(),
        page=2,
        limit=50
    ))

- **Get active API keys:**

.. code-block:: python

    >>> api_keys = bsx_instance.get_api_key_list()

- **Delete an API key:**

.. code-block:: python

    >>> bsx_instance.delete_user_api_key(api_key="eac9756c3ac0540d74c4bb897a68846a")

- **Create a new API key:**

.. code-block:: python

    >>> api_key = bsx_instance.create_user_api_key(name='test API key')

- **Get all markets:**

.. code-block:: python

    >>> products = bsx_instance.get_products()

Async APIs
------------
Below are async APIs to interact with BSX Exchange

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
    >>> order = await bsx_instance.create_order_async(params=params)

- **Cancel an order:**

.. code-block:: python

    >>> res = await bsx_instance.cancel_order_async(order_id="xxx")

- **Cancel multiple orders:**

.. code-block:: python

    >>> res = await bsx_instance.cancel_bulk_orders_async(order_ids=["xxx", "yyy"])

- **Cancel all open orders:**

.. code-block:: python

    >>> res = await bsx_instance.cancel_all_orders_async(product_id="BTC-PERP")

- **Update orders in batch:**

.. code-block:: python

    >>> from bsx_py.common.types.market import *
    >>> params = BatchOrderUpdateParams(operations=[
        CreateOrderParams(
            type=OrderType.LIMIT,
            side=Side.BUY,
            product_index=3,
            price=Decimal('100.3'),
            size=Decimal('0.1'),
            time_inf_force='GTC',
            nonce=int(time.time_ns()),
            post_only=false,
            client_order_id='522005f7bfdb48c98b931a40296cdf96'
        ),
        CancelOrderParams(order_id="8a325a62-80f0-46ef-8943-3267b381271f"),
        CancelAllParams(product_id="SOL-PERP"),
        CancelOrdersParams(order_ids=['8a325a62-80f0-46ef-8943-3267b381271f'])
    ])
    >>> res = await bsx_instance.batch_update_orders_async(params)

- **Get all open orders:**

.. code-block:: python

    >>> res = await bsx_instance.get_all_open_orders_async(product_id="BTC-PERP")

- **Get order history:**

.. code-block:: python

    >>> from bsx_py.common.types.market import *
    >>> params = GetOrderHistoryParams(
        product_id="SOL-PERP",
        start_time=datetime.now() - timedelta(days=30),
        end_time=datetime.now(),
        limit=100,
        statuses=[OrderStatus.DONE, OrderStatus.OPEN, OrderStatus.PENDING],
        client_order_id=["abc", "xyz"]
    )
    >>> history = await bsx_instance.get_order_history_async(params)

- **Submit withdrawal request:**

.. code-block:: python

    >>> from bsx_py.common.types.account import *
    >>> params = WithdrawParams(
        amount=Decimal("10"),
        nonce=int(time.time_ns())
    )
    >>> is_success = await bsx_instance.submit_withdrawal_request_async(params)

- **Get portfolio detail:**

.. code-block:: python

    >>> portfolio = await bsx_instance.get_portfolio_detail_async()

- **Get trade history:**

.. code-block:: python

    >>> from bsx_py.common.types.market import *
    >>> history = await bsx_instance.get_user_trade_history_async(params=GetTradeHistoryParams(
        product_id='BTC-PERP',
        start_time=datetime.now() - timedelta(days=1),
        end_time=datetime.now(),
        page=1,
        limit=50
    ))

- **Get funding rate history:**

.. code-block:: python

    >>> from bsx_py.common.types.market import *
    >>> history = await bsx_instance.get_funding_history_async(params=GetFundingHistoryParams(
        product_id='BTC-PERP',
        start_time=datetime.now() - timedelta(days=1),
        end_time=datetime.now(),
        page=2,
        limit=50
    ))

- **Get active API keys:**

.. code-block:: python

    >>> api_keys = await bsx_instance.get_api_key_list_async()

- **Delete an API key:**

.. code-block:: python

    >>> await bsx_instance.delete_user_api_key_async(api_key="eac9756c3ac0540d74c4bb897a68846a")

- **Create a new API key:**

.. code-block:: python

    >>> api_key = await bsx_instance.create_user_api_key_async(name='test API key')

- **Get all markets:**

.. code-block:: python

    >>> products = await bsx_instance.get_products_async()

