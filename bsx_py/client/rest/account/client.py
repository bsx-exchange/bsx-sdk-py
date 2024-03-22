import time

from eip712_structs import EIP712Struct
from eth_account import Account
from web3 import Web3

from bsx_py.client.rest.account.types import SignKey, Register, Withdraw
from bsx_py.client.rest.base import RestClient, AuthRequiredClient
from bsx_py.common import X18_DECIMALS
from bsx_py.common.types.account import RegisterParams, BSXApiKey, WithdrawParams, Portfolio
from bsx_py.common.utils import AccountStorage


class RegistrationClient(RestClient):
    _domain_signature: EIP712Struct

    def __init__(self, domain: str, domain_signature: EIP712Struct):
        super().__init__(domain)
        self._domain_signature = domain_signature

    def register(self, params: RegisterParams) -> BSXApiKey:
        wallet = Account.from_key(params.wallet_pkey)
        signer = Account.from_key(params.signer_pkey)

        signable_wallet = SignKey(account=wallet.address)
        signable_signer_bytes = Web3.keccak(signable_wallet.signable_bytes(domain=self._domain_signature))
        signer_signature = Account._sign_hash(signable_signer_bytes, signer.key).signature.hex()

        nonce = round(time.time())
        signable_message = Register(key=signer.address, message=params.message, nonce=nonce)
        signable_message_bytes = Web3.keccak(signable_message.signable_bytes(domain=self._domain_signature))
        account_signature = Account._sign_hash(signable_message_bytes, wallet.key).signature.hex()

        payload = {
            "user_wallet": wallet.address,
            "signer": signer.address,
            "nonce": nonce,
            "wallet_signature": account_signature,
            "signer_signature": signer_signature,
            "message": params.message,
        }

        resp = self.post("/users/register", payload)
        return BSXApiKey(**resp)


class AccountClient(AuthRequiredClient):
    _domain_signature: EIP712Struct

    def __init__(self, domain: str, domain_signature: EIP712Struct, config, acc_storage: AccountStorage):
        super().__init__(domain, acc_storage)
        self._domain_signature = domain_signature
        self._config = config
        self._acc_storage = acc_storage

    def submit_withdrawal_request(self, params: WithdrawParams) -> bool:
        usdc_address = self._config["addresses"]["usdc_contract"]
        withdraw_struct = Withdraw(
            sender=self._acc_storage.get_wallet_address(),
            token=usdc_address,
            amount=int(params.amount * X18_DECIMALS),
            nonce=params.nonce,
        )

        withdraw_struct_bytes = Web3.keccak(
            withdraw_struct.signable_bytes(domain=self._domain_signature)
        )
        withdraw_signature = Account._sign_hash(
            withdraw_struct_bytes, self._acc_storage.get_wallet_key()
        ).signature.hex()

        payload = {
            "sender": self._acc_storage.get_wallet_address(),
            "token": usdc_address,
            "amount": str(params.amount),
            "nonce": params.nonce,
            "signature": withdraw_signature,
        }

        resp = self.post("/transfers/withdraw", payload)
        return resp["success"]

    def get_portfolio_detail(self) -> Portfolio:
        resp = self.get("/portfolio/detail")
        return Portfolio.from_dict(resp)
