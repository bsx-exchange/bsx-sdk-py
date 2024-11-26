import json

from eip712_structs import EIP712Struct
from eth_account import Account
from web3 import Web3

from bsx_py.client.rest.account.types import Withdraw
from bsx_py.client.rest.base import AuthRequiredClient
from bsx_py.common import X18_DECIMALS
from bsx_py.common.acc_info import AccountInfo
from bsx_py.common.types.account import *


class AccountClient(AuthRequiredClient):
    _domain_signature: EIP712Struct

    def __init__(self, domain: str, domain_signature: EIP712Struct, config, acc_info: AccountInfo):
        super().__init__(domain, acc_info)
        self._domain_signature = domain_signature
        self._config = config
        self._acc_info = acc_info

    def submit_withdrawal_request(self, params: WithdrawParams) -> bool:
        usdc_address = self._config["addresses"]["usdc_contract"]
        withdraw_struct = Withdraw(
            sender=self._acc_info.get_wallet_address(),
            token=usdc_address,
            amount=int(params.amount * X18_DECIMALS),
            nonce=params.nonce,
        )

        withdraw_struct_bytes = Web3.keccak(
            withdraw_struct.signable_bytes(domain=self._domain_signature)
        )
        withdraw_signature = Account._sign_hash(
            withdraw_struct_bytes, self._acc_info.get_wallet_key()
        ).signature.hex()

        payload = {
            "sender": self._acc_info.get_wallet_address(),
            "token": usdc_address,
            "amount": str(params.amount),
            "nonce": params.nonce,
            "signature": withdraw_signature,
        }

        resp = self.post("/transfers/withdraw", payload)
        return resp["success"]

    async def submit_withdrawal_request_async(self, params: WithdrawParams) -> bool:
        usdc_address = self._config["addresses"]["usdc_contract"]
        withdraw_struct = Withdraw(
            sender=self._acc_info.get_wallet_address(),
            token=usdc_address,
            amount=int(params.amount * X18_DECIMALS),
            nonce=params.nonce,
        )

        withdraw_struct_bytes = Web3.keccak(
            withdraw_struct.signable_bytes(domain=self._domain_signature)
        )
        withdraw_signature = Account._sign_hash(
            withdraw_struct_bytes, self._acc_info.get_wallet_key()
        ).signature.hex()

        payload = {
            "sender": self._acc_info.get_wallet_address(),
            "token": usdc_address,
            "amount": str(params.amount),
            "nonce": params.nonce,
            "signature": withdraw_signature,
        }

        resp = await self.post_async("/transfers/withdraw", payload)
        return resp["success"]

    def get_portfolio_detail(self) -> Portfolio:
        resp = self.get("/portfolio/detail")
        return Portfolio.from_dict(resp)

    async def get_portfolio_detail_async(self) -> Portfolio:
        resp = await self.get_async("/portfolio/detail")
        return Portfolio.from_dict(resp)

    def get_api_key_list(self) -> GetAPIKeysResponse:
        resp = self.get("/users/api-key")
        return GetAPIKeysResponse.from_dict(resp)

    async def get_api_key_list_async(self) -> GetAPIKeysResponse:
        resp = await self.get_async("/users/api-key")
        return GetAPIKeysResponse.from_dict(resp)

    def delete_user_api_key(self, api_key: str) -> str:
        resp = self.delete("/users/api-key", params={"api_keys": [api_key]})
        if 'api_keys' in resp and api_key in resp['api_keys']:
            return api_key
        else:
            raise Exception("API key not found in response. Actual response: " + json.dumps(resp))

    async def delete_user_api_key_async(self, api_key: str) -> str:
        resp = await self.delete_async("/users/api-key", params={"api_keys": [api_key]})
        if 'api_keys' in resp and api_key in resp['api_keys']:
            return api_key
        else:
            raise Exception("API key not found in response. Actual response: " + json.dumps(resp))

    def create_user_api_key(self, name: str = "") -> APIKey:
        resp = self.post("/users/api-key", body={"name": name})
        if "api_key" in resp:
            return APIKey.from_dict(resp["api_key"])
        else:
            raise Exception("API key not found in response. Actual response: " + json.dumps(resp))

    async def create_user_api_key_async(self, name: str = "") -> APIKey:
        resp = await self.post_async("/users/api-key", body={"name": name})
        if "api_key" in resp:
            return APIKey.from_dict(resp["api_key"])
        else:
            raise Exception("API key not found in response. Actual response: " + json.dumps(resp))

    def update_collateral_mode(self, collateral_mode: CollateralMode) -> bool:
        resp = self.post("/collateral-mode", body={"collateral_mode": collateral_mode})
        if "success" in resp:
            return resp["success"]
        else:
            raise Exception(json.dumps(resp))

    async def update_collateral_mode_async(self, collateral_mode: CollateralMode) -> bool:
        resp = await self.post_async("/collateral-mode", body={"collateral_mode": collateral_mode})
        if "success" in resp:
            return resp["success"]
        else:
            raise Exception(json.dumps(resp))

    def update_margin_mode(self, product_id: str, margin_mode: MarginMode) -> bool:
        resp = self.post("/margin-mode", body={"product_id": product_id, "margin_mode": margin_mode})
        if "success" in resp:
            return resp["success"]
        else:
            raise Exception(json.dumps(resp))

    async def update_margin_mode_async(self, product_id: str, margin_mode: MarginMode) -> bool:
        resp = await self.post_async("/margin-mode", body={"product_id": product_id, "margin_mode": margin_mode})
        if "success" in resp:
            return resp["success"]
        else:
            raise Exception(json.dumps(resp))

    def update_leverage(self, product_id: str, leverage: float) -> bool:
        resp = self.post("/leverage", body={"product_id": product_id, "leverage": leverage})
        if "success" in resp:
            return resp["success"]
        else:
            raise Exception(json.dumps(resp))

    async def update_leverage_async(self, product_id: str, leverage: float) -> bool:
        resp = await self.post_async("/leverage", body={"product_id": product_id, "leverage": leverage})
        if "success" in resp:
            return resp["success"]
        else:
            raise Exception(json.dumps(resp))
