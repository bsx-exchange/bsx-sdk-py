import asyncio
from http import client
import time

from eth_account import Account
from bsx_py.common.types.market import (
    BatchOrderUpdateParams,
    CancelAllParams,
    CancelOrderParams,
    CreateOrderParams,
    OrderType,
    Side,
)
from bsx_py.instance import BSXInstance, Environment


async def create(bsx_instance: BSXInstance):
    try:
        params = CreateOrderParams(
            side=Side.BUY,
            type=OrderType.LIMIT,
            product_index=1,
            price=80000,
            size=0.1,
            time_in_force="GTC",
            nonce=int(time.time_ns()),
        )
        order = await bsx_instance.create_order_async(params)
        print(order)
    except Exception as e:
        print(e)


async def cancel(bsx_instance: BSXInstance):
    try:
        # cancel by id
        result = await bsx_instance.cancel_order_async(
            order_id="62bd5069-8450-4015-b7ca-abb034054cd0",
        )
        print(result)

        # cancel all orders of a specific product
        result = await bsx_instance.cancel_all_orders_async(product_id="BTC-PERP")
        print(result)
        pass
    except Exception as e:
        print(e)


async def batch(bsx_instance: BSXInstance):
    try:
        order0 = await bsx_instance.create_order_async(
            CreateOrderParams(
                side=Side.BUY,
                type=OrderType.LIMIT,
                product_index=1,
                price=80000,
                size=0.1,
                time_in_force="GTC",
                nonce=int(time.time_ns()),
            )
        )
        print(order0)
        print("===")
        result = await bsx_instance.batch_update_orders_async(
            BatchOrderUpdateParams(
                [
                    CancelAllParams(product_id="BTC-PERP"),
                    CreateOrderParams(
                        side=Side.BUY,
                        type=OrderType.LIMIT,
                        product_index=1,
                        price=79000,
                        size=0.1,
                        time_in_force="GTC",
                        nonce=int(time.time_ns()),
                    ),
                ]
            )
        )
        print(result)
    except Exception as e:
        print(e)


async def main():
    bsx_instance = BSXInstance.from_api_key(
        api_key="7de31802d6bbd54230db0c3ac0c996a7",
        api_secret="ba1b31a16363a16916e695269d90925e3c5501d67fe89329be476c52bddd5a23",
        signer=Account.from_key(
            "0x746de15abd290263318d37e877c0c97e1138c5907eae7c5171b124039e77be2b"
        ),
        env=Environment.TESTNET,
    )

    # NOTE: this is another way to init bsx client
    # bsx_instance = BSXInstance(
    #     env=Environment.TESTNET,
    #     wallet=Account.from_key(
    #         "0x75ce163a131b85066a8c9c69ca209b5898062dad91fe1ca153750f4ca58dcd3e"
    #     ),
    #     signer=Account.from_key(
    #         "0xb318e3cf7ae1abf758ae6d0b965298bcd87e6b49a9aabaae03606acc391b7e24"
    #     ),
    # )

    print("### create")
    await create(bsx_instance=bsx_instance)
    print("### cancel")
    await cancel(bsx_instance=bsx_instance)
    print("### batch")
    await batch(bsx_instance=bsx_instance)


asyncio.run(main())
