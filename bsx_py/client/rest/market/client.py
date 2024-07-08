import json
import time
from typing import Optional

from eip712_structs import EIP712Struct
from eth_account import Account
from web3 import Web3

from bsx_py.client.rest.base import AuthRequiredClient
from bsx_py.client.rest.market.types import Order as EIP712Order
from bsx_py.common import X18_DECIMALS
from bsx_py.common.acc_info import AccountInfo
from bsx_py.common.types.market import *
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
            "statuses": [s.value for s in params.statuses] if params.statuses is not None else None,
            "client_order_ids": params.client_order_ids
        }

        resp = self.get("/order-history", params=rest_params)

        return OrderListingResult(
            orders=[Order.from_dict(i) for i in resp]
        )

    def batch_update_orders(self, params: BatchOrderUpdateParams) -> BatchOrderUpdateResponse:
        operations = []
        for p in params.operations:
            if isinstance(p, CreateOrderParams):
                order_struct = EIP712Order(
                    sender=self._acc_storage.get_wallet_address(),
                    size=int(p.size * X18_DECIMALS),
                    price=int(p.price * X18_DECIMALS),
                    nonce=p.nonce,
                    productIndex=p.product_index,
                    orderSide=1 if p.side == Side.SELL else 0
                )
                signable_bytes = Web3.keccak(order_struct.signable_bytes(domain=self._domain_signature))

                signature = Account._sign_hash(signable_bytes, self._acc_storage.get_signer_key()).signature.hex()

                payload = {
                    "side": p.side.value,
                    "type": p.type.value,
                    "product_index": p.product_index,
                    "price": str(p.price),
                    "size": str(p.size),
                    "post_only": p.post_only,
                    "reduce_only": p.reduce_only,
                    "time_in_force": p.time_in_force,
                    "nonce": p.nonce,
                    "signature": signature,
                    "client_order_id": p.client_order_id
                }

                operations.append({"op_type": "CREATE", "create_order_request": payload})
            elif isinstance(p, CancelOrderParams):
                operations.append({"op_type": "CANCEL", "cancel_request": {
                    "order_id": p.order_id,
                    "nonce": p.nonce,
                    "client_order_id": p.client_order_id
                }})
            elif isinstance(p, CancelOrdersParams):
                operations.append({"op_type": "CANCEL_BULK", "cancel_orders_request": {
                    "order_ids": p.order_ids,
                    "nonces": p.nonces,
                    "client_order_ids": p.client_order_ids
                }})
            elif isinstance(p, CancelAllParams):
                operations.append({"op_type": "CANCEL_ALL", "cancel_all_orders_request": {
                    "product_id": p.product_id
                }})

        resp = self.post(endpoint="/orders/batch", body={"data": operations})
        return BatchOrderUpdateResponse.from_dict(resp)

    def get_user_trade_history(self, params: GetTradeHistoryParams) -> GetTradeHistoryResponse:
        rest_params = {
            "product_id": params.product_id,
            "start_time": int(time.mktime(params.start_time.timetuple())) * 1000000000 if params.start_time is not None else None,
            "end_time": int(time.mktime(params.end_time.timetuple())) * 1000000000 if params.end_time is not None else None,
            "limit": params.limit,
            "page": params.page,
        }
        resp = self.get("/trade-history", params=rest_params)
        return GetTradeHistoryResponse.from_dict(resp)

    def get_products(self) -> GetProductsResponse:
        resp = self.get("/products")
        return GetProductsResponse.from_dict(resp)

    def get_funding_history(self, params: GetFundingHistoryParams) -> GetFundingHistoryResponse:
        endpoint = "/products/" + params.product_id + "/funding-rate"
        rest_params = {
            "from": int(time.mktime(params.start_time.timetuple())) * 1000000000 if params.start_time is not None else None,
            "to": int(time.mktime(params.end_time.timetuple())) * 1000000000 if params.end_time is not None else None,
            "limit": params.limit,
            "page": params.page,
        }
        resp = self.get(endpoint, params=rest_params)
        return GetFundingHistoryResponse.from_dict(resp)
