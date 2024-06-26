from eip712_structs import EIP712Struct
from eth_account import Account
from web3 import Web3

from bsx_py.client.rest.account.types import Withdraw
from bsx_py.client.rest.base import AuthRequiredClient
from bsx_py.common import X18_DECIMALS
from bsx_py.common.acc_info import AccountInfo
from bsx_py.common.types.account import WithdrawParams, Portfolio


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

    def get_portfolio_detail(self) -> Portfolio:
        resp = self.get("/portfolio/detail")
        return Portfolio.from_dict(resp)
