import _thread
import asyncio
import base64
import hashlib
import hmac
import threading
import time
from datetime import timedelta
from decimal import Decimal

import pandas
from eth_account import Account
from bsx_py import BSXInstance, Environment
from bsx_py.common.types.account import WithdrawParams
from bsx_py.common.types.market import *


def new_order(b, n):
    try:
        print(b.create_order(params=CreateOrderParams(
            type=OrderType.LIMIT,
            side=Side.BUY,
            product_index=3,
            price=Decimal("156"),
            size=Decimal("2.5"),
            time_in_force="GTC",
            # nonce=n,
            nonce=int(time.time() * 1e9),
            post_only=True,
        )))
    except Exception as e:
        print(e)


async def main():
    # wallet_private_key = "0x75ce163a131b85066a8c9c69ca209b5898062dad91fe1ca153750f4ca58dcd3e" # multi sig
    # wallet_private_key = "0xb318e3cf7ae1abf758ae6d0b965298bcd87e6b49a9aabaae03606acc391b7e24" # empty acc
    wallet_private_key = "0x497cb75972414c032715536153426c07ac59e8600b7883115de2d6edde72d4c4"  # eth maker 1
    signer_private_key = "0xb318e3cf7ae1abf758ae6d0b965298bcd87e6b49a9aabaae03606acc391b7e24"
    wallet = Account.from_key(wallet_private_key)
    signer = Account.from_key(signer_private_key)
    # bsx_instance = BSXInstance(env="https://api.dev.bsx.exchange", wallet=wallet, signer=signer)
    bsx_instance = BSXInstance(env="http://localhost:8090", wallet=wallet, signer=signer)

    # bsx_instance = BSXInstance.from_multi_sig_wallet(env="http://localhost:8090", contract=wallet, signer=signer, owner_address="0x9fF6E36Cf97A01b169a5e6E351ab1375955271A3")
    # bsx_instance = BSXInstance.from_api_key(env="http://localhost:8090", api_key="764b24c65762509b2f85e5082264bfe1",
    #                                         api_secret="79b9ff5dd151b6f4b72b5b309b7a1a0780316e18c5bf51b10c57b0bbc8764b1b",
    #                                         signer=signer)
    async def test1():
        print(await bsx_instance.batch_update_orders_async(
            params=BatchOrderUpdateParams(operations=[
                # CreateOrderParams(
                #     type=OrderType.LIMIT,
                #     side=Side.BUY,
                #     product_index=3,
                #     price=Decimal("10"),
                #     size=Decimal("2.5"),
                #     time_in_force="GTC",
                #     nonce=int(time.time_ns()),
                #     post_only=False,
                #     client_order_id="127"
                # ),
                CancelOrderParams(nonce="456"),
                # CancelAllParams(product_id="BTC-PERP"),
                # CancelOrdersParams(client_order_ids=['127'])
            ])
        ))

    async def test2():
        print(await bsx_instance.batch_update_orders_async(
            params=BatchOrderUpdateParams(operations=[
                # CreateOrderParams(
                #     type=OrderType.LIMIT,
                #     side=Side.BUY,
                #     product_index=3,
                #     price=Decimal("10"),
                #     size=Decimal("2.5"),
                #     time_in_force="GTC",
                #     nonce=int(time.time_ns()),
                #     post_only=False,
                #     client_order_id="127"
                # ),
                CancelOrderParams(nonce="123"),
                # CancelAllParams(product_id="BTC-PERP"),
                # CancelOrdersParams(client_order_ids=['127'])
            ])
        ))

    await asyncio.gather(test1(), test2())

asyncio.run(main())
