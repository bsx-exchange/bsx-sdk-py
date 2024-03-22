from eth_account.signers.local import LocalAccount

from bsx_py.common.lock import ReadWriteLock
from bsx_py.common.types.account import BSXApiKey


class AccountStorage:
    _api_key: BSXApiKey
    _wallet: LocalAccount
    _signer: LocalAccount

    def __init__(self):
        self._rwLock = ReadWriteLock(write_promotion=True)

    def lock_all_read(self) -> bool:
        return self._rwLock.acquire_write_no_wait()

    def release_all_read(self):
        self._rwLock.release_write()

    def set_api_key(self, api_key: BSXApiKey):
        self._api_key = api_key

    def set_wallet(self, wallet: LocalAccount):
        self._wallet = wallet

    def set_signer(self, signer: LocalAccount):
        self._signer = signer

    def get_api_key(self) -> BSXApiKey:
        try:
            self._rwLock.acquire_read()
            return self._api_key
        finally:
            self._rwLock.release_read()

    def get_wallet_address(self):
        return self._wallet.address

    def get_wallet_key(self):
        return self._wallet.key

    def get_signer_key(self):
        return self._signer.key