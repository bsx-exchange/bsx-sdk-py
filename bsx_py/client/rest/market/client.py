import time
from typing import Optional

from eip712_structs import EIP712Struct
from eth_account import Account
from web3 import Web3

from bsx_py.client.rest.base import AuthRequiredClient
from bsx_py.client.rest.market.types import Order as EIP712Order
from bsx_py.common import X18_DECIMALS
from bsx_py.common.acc_info import AccountInfo
from bsx_py.common.types.market import CreateOrderParams, Side, CancelOrderResult, CancelMultipleOrdersParams, \
    CancelMultipleOrdersResult, OrderListingResult, GetOrderHistoryParams
from bsx_py.common.types.market import Order


class MarketClient(AuthRequiredClient):
    def __init__(self, domain: str, domain_signature: EIP712Struct, acc_info: AccountInfo):
        super().__init__(domain, acc_info)
        self._domain_signature = domain_signature
        self._acc_storage = acc_info

    def create_order(self, params: CreateOrderParams) -> Order:
        order_struct = EIP712Order(
            sender=self._acc_storage.get_wallet_address(),
            size=int(params.size * X18_DECIMALS),
            price=int(params.price * X18_DECIMALS),
            nonce=params.nonce,
            productIndex=params.product_index,
            orderSide=1 if params.side == Side.SELL else 0
        )
        signable_bytes = Web3.keccak(order_struct.signable_bytes(domain=self._domain_signature))

        signature = Account._sign_hash(signable_bytes, self._acc_storage.get_signer_key()).signature.hex()

        payload = {
            "side": params.side.value,
            "type": params.type.value,
            "product_index": params.product_index,
            "price": str(params.price),
            "size": str(params.size),
            "post_only": params.post_only,
            "reduce_only": params.reduce_only,
            "time_in_force": params.time_in_force,
            "nonce": params.nonce,
            "signature": signature,
        }

        resp = self.post(endpoint="/orders", body=payload)
        return Order.from_dict(resp)

    def cancel_order(self, order_id: Optional[str] = None, nonce: Optional[int] = None) -> CancelOrderResult:
        resp = self.delete(endpoint="/order", params={"order_id": order_id, "nonce": nonce})
        return CancelOrderResult.from_dict(resp)

    def cancel_orders(self, params: CancelMultipleOrdersParams):
        payload = {
            "product_ids": params.product_ids,
            "order_ids": params.order_ids,
            "nonces": params.nonces
        }

        resp = self.delete(endpoint="/orders", body=payload)
        return CancelMultipleOrdersResult(
            cancelled_orders=[
                CancelOrderResult(order_id=i.get("id"), nonce=i.get("nonce"))
                for i in resp.get("cancel_requested_orders")
            ]
        )

    def cancel_all_orders(self, product_id: str) -> CancelMultipleOrdersResult:
        payload = {
            "product_id": product_id
        }

        resp = self.delete(endpoint="/orders/all", params=payload)
        return CancelMultipleOrdersResult(
            cancelled_orders=[
                CancelOrderResult(order_id=i.get("order_id"), nonce=i.get("nonce"))
                for i in resp.get("cancel_requested_orders")
            ]
        )

    def get_all_open_orders(self, product_id: str) -> OrderListingResult:
        resp = self.get("/orders", params={"product_id": product_id})
        return OrderListingResult(
            orders=[Order.from_dict(i) for i in resp]
        )

    def get_order_history(self, params: GetOrderHistoryParams) -> OrderListingResult:
        rest_params = {
            "product_id": params.product_id,
            "start_time": int(time.mktime(params.start_time.timetuple())) * 1000000000 if params.start_time is not None
            else None,
            "end_time": int(time.mktime(params.end_time.timetuple())) * 1000000000 if params.end_time is not None
            else None,
            "limit": params.limit if params.limit is not None else 100,
            "statuses": [s.value for s in params.statuses] if params.statuses is not None else None
        }

        resp = self.get("/order-history", params=rest_params)

        return OrderListingResult(
            orders=[Order.from_dict(i) for i in resp]
        )
