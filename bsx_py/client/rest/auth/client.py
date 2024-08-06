import time

from eip712_structs import EIP712Struct
from eth_account import Account
from web3 import Web3

from bsx_py.common.types.auth import *
from .types import SignKey, Register
from ..base import RestClient


class AuthClient(RestClient):
    _domain_signature: EIP712Struct

    def __init__(self, domain: str, domain_signature: EIP712Struct):
        super().__init__(domain)
        self._domain_signature = domain_signature

    def register_with_existing_signature(self, params: RegisterWithExistSignatureParams) -> Register:
        signer = Account.from_key(params.signer_pkey)
        signable_wallet = SignKey(account=params.wallet_addr)
        signable_signer_bytes = Web3.keccak(signable_wallet.signable_bytes(domain=self._domain_signature))
        signer_signature = Account._sign_hash(signable_signer_bytes, signer.key).signature.hex()

        payload = {
            "user_wallet": params.wallet_addr,
            "signer": signer.address,
            "nonce": params.nonce,
            "wallet_signature": params.signature,
            "signer_signature": signer_signature,
            "message": "Please sign in with your wallet to access bsx.exchange. You are signing in on %d. "
                       "This message is exclusively signed with bsx.exchange for security." % params.nonce,
        }

        resp = self.post("/users/register", payload)
        return BSXApiKey.from_dict(resp)

    def register(self, params: RegisterParams) -> BSXApiKey:
        wallet = Account.from_key(params.wallet_pkey)
        signer = Account.from_key(params.signer_pkey)

        signable_wallet = SignKey(account=params.wallet_addr)
        signable_signer_bytes = Web3.keccak(signable_wallet.signable_bytes(domain=self._domain_signature))
        signer_signature = Account._sign_hash(signable_signer_bytes, signer.key).signature.hex()

        nonce = round(time.time_ns())
        signable_message = Register(key=signer.address, message=params.message, nonce=nonce)
        signable_message_bytes = Web3.keccak(signable_message.signable_bytes(domain=self._domain_signature))
        account_signature = Account._sign_hash(signable_message_bytes, wallet.key).signature.hex()

        payload = {
            "user_wallet": params.wallet_addr,
            "signer": signer.address,
            "nonce": nonce,
            "wallet_signature": account_signature,
            "signer_signature": signer_signature,
            "message": params.message,
        }

        resp = self.post("/users/register", payload)
        return BSXApiKey.from_dict(resp)

    def create_new_api_key(self, api_key: str, api_secret: str) -> BSXApiKeyDetail:
        headers = {
            "bsx-key": api_key,
            "bsx-secret": api_secret
        }
        body = {
            "name": ""
        }

        resp = self.post("/users/api-key", body=body, headers=headers)

        return BSXApiKeyDetail.from_dict(resp["api_key"])

    def get_api_key_detail(self, api_key: str, api_secret: str) -> BSXApiKeyDetail:
        headers = {
            "bsx-key": api_key,
            "bsx-secret": api_secret
        }

        resp = self.get("/users/api-key", headers=headers)

        for key_detail in resp["api_keys"]:
            if key_detail["api_key"] == api_key:
                return BSXApiKeyDetail.from_dict(key_detail)

        raise Exception("API key does not exist or is expired")
