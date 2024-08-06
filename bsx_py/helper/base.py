from abc import abstractmethod

from eip712_structs import EIP712Struct

from bsx_py.client.rest.auth.client import AuthClient
from bsx_py.common.types.auth import BSXApiKey
from .acc_storage import AccountStorage
from ..common.acc_info import AccountInfo


class AccountManager(AccountInfo):
    def __init__(self, domain: str, domain_signature: EIP712Struct):
        self._auth_client = AuthClient(domain, domain_signature)
        self._acc_storage = AccountStorage()

    @staticmethod
    def from_secret(wallet_secret: str, signer_secret: str, domain: str, domain_signature: EIP712Struct):
        from .secret_base_manager import SecretBaseManager
        return SecretBaseManager(wallet_secret, signer_secret, domain, domain_signature)

    @staticmethod
    def from_api_key(api_key: str, api_secret: str, signer_secret: str, domain: str, domain_signature: EIP712Struct):
        from .api_key_base_manager import ApiKeyBaseManager
        return ApiKeyBaseManager(api_key, api_secret, signer_secret, domain, domain_signature)

    @staticmethod
    def from_smart_contract(contract_address: str, signature: str, nonce: int, signer_secret: str, domain: str, domain_signature: EIP712Struct):
        from .signature_base_manager import SignatureBaseManager
        return SignatureBaseManager(contract_address, signature, nonce, signer_secret, domain, domain_signature)

    def get_api_key(self) -> BSXApiKey:
        return self._acc_storage.get_api_key()

    def get_wallet_address(self):
        return self._acc_storage.get_wallet_address()

    def get_wallet_key(self):
        return self._acc_storage.get_wallet_key()

    def get_signer_key(self):
        return self._acc_storage.get_signer_key()

    @abstractmethod
    def check_and_renew_api_key(self):
        raise NotImplementedError

    def renew_api_key(self):
        self._acc_storage.lock_all_read()
        try:
            self._renew_api_key()
        finally:
            self._acc_storage.release_all_read()

    @abstractmethod
    def _renew_api_key(self):
        raise NotImplementedError
