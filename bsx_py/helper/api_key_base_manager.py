from datetime import datetime, timedelta

from .base import AccountManager
from ..common.exception import WalletPrivateNotProvidedException
from ..common.types.auth import BSXApiKey
from eth_account import Account


class EIP712Struct:
    pass


class ApiKeyBaseManager(AccountManager):
    def __init__(self, api_key: str, api_secret: str, signer_secret: str, domain: str, domain_signature: EIP712Struct):
        super().__init__(domain, domain_signature)
        api_key_detail = self._auth_client.get_api_key_detail(api_key=api_key, api_secret=api_secret)
        self._acc_storage.set_api_key(BSXApiKey(
            api_key=api_key,
            api_secret=api_secret,
            expired_at=api_key_detail.expired_at,
            name=api_key_detail.name
        ))
        signer = Account.from_key(signer_secret)
        self._acc_storage.set_signer_addr(signer.address)
        self._acc_storage.set_signer_pkey(signer.key)
        self._acc_storage.set_wallet_addr(api_key_detail.sender)

    def get_wallet_key(self):
        raise WalletPrivateNotProvidedException()

    def check_and_renew_api_key(self):
        current_api_key = self._acc_storage.get_api_key()
        if current_api_key.expired_at < datetime.now() + timedelta(minutes=5):
            self.renew_api_key()

    def renew_api_key(self):
        self._acc_storage.lock_all_read()
        try:
            current_api_key = self._acc_storage.get_api_key()
            new_api_key = self._auth_client.create_new_api_key(current_api_key.api_key, current_api_key.api_secret)
            self._acc_storage.set_api_key(BSXApiKey(
                api_key=new_api_key.api_key,
                api_secret=new_api_key.api_secret,
                expired_at=new_api_key.expired_at,
                name=new_api_key.name
            ))
        finally:
            self._acc_storage.release_all_read()
