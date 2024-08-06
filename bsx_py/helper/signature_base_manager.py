from datetime import datetime, timedelta

from eth_account import Account

from .api_key_base_manager import EIP712Struct
from .base import AccountManager
from ..common.exception import WalletPrivateNotProvidedException
from ..common.types.auth import BSXApiKey, RegisterWithExistSignatureParams


class SignatureBaseManager(AccountManager):
    def __init__(self, wallet_addr: str, signature: str, nonce: int, signer_secret: str, domain: str,
                 domain_signature: EIP712Struct):
        super().__init__(domain, domain_signature)
        signer = Account.from_key(signer_secret)
        api_key = self._auth_client.register_with_existing_signature(
            RegisterWithExistSignatureParams(
                wallet_addr=wallet_addr, signature=signature, nonce=nonce, signer_pkey=signer_secret
            )
        )
        self._acc_storage.set_signer_addr(signer.address)
        self._acc_storage.set_signer_pkey(signer.key)
        self._acc_storage.set_wallet_addr(wallet_addr)
        self._acc_storage.set_api_key(api_key)

    def get_wallet_key(self):
        raise WalletPrivateNotProvidedException()

    def check_and_renew_api_key(self):
        current_api_key = self._acc_storage.get_api_key()
        if current_api_key.expired_at < datetime.now() + timedelta(minutes=5):
            self.renew_api_key()

    def _renew_api_key(self):
        current_api_key = self._acc_storage.get_api_key()
        new_api_key = self._auth_client.create_new_api_key(current_api_key.api_key, current_api_key.api_secret)
        self._acc_storage.set_api_key(BSXApiKey(
            api_key=new_api_key.api_key,
            api_secret=new_api_key.api_secret,
            expired_at=new_api_key.expired_at,
            name=new_api_key.name
        ))
