from .api_key_base_manager import EIP712Struct
from .base import AccountManager
from ..common.types.auth import BSXApiKey, RegisterParams
from eth_account import Account


class SecretBaseManager(AccountManager):
    def __init__(self, wallet_secret: str, signer_secret: str, domain: str, domain_signature: EIP712Struct):
        super().__init__(domain, domain_signature)
        wallet = Account.from_key(wallet_secret)
        signer = Account.from_key(signer_secret)
        api_key = self._auth_client.register(
            RegisterParams(wallet_pkey=wallet_secret, signer_pkey=signer_secret, message="")
        )
        self._acc_storage.set_signer_addr(signer.address)
        self._acc_storage.set_signer_pkey(signer.key)
        self._acc_storage.set_wallet_addr(wallet.address)
        self._acc_storage.set_wallet_pkey(wallet.key)
        self._acc_storage.set_api_key(api_key)

    def check_and_renew_api_key(self):
        pass

    def renew_api_key(self):
        self._acc_storage.lock_all_read()
        try:
            params = RegisterParams(
                wallet_pkey=self._acc_storage.get_wallet_key(),
                signer_pkey=self._acc_storage.get_signer_key(),
                message=""
            )
            new_api_key = self._auth_client.register(params)
            self._acc_storage.set_api_key(new_api_key)
        finally:
            self._acc_storage.release_all_read()
