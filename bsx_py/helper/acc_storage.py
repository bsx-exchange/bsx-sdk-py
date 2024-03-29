from bsx_py.common.lock import ReadWriteLock
from bsx_py.common.types.auth import BSXApiKey


class AccountStorage:
    _api_key: BSXApiKey
    _wallet_addr: str
    _wallet_pkey: str
    _signer_addr: str
    _signer_pkey: str

    def __init__(self):
        self._rwLock = ReadWriteLock(write_promotion=True)

    def lock_all_read(self) -> bool:
        return self._rwLock.acquire_write_no_wait()

    def release_all_read(self):
        self._rwLock.release_write()

    def set_api_key(self, api_key: BSXApiKey):
        self._api_key = api_key

    def set_wallet_addr(self, wallet_addr: str):
        self._wallet_addr = wallet_addr

    def set_signer_addr(self, signer_addr: str):
        self._signer_addr = signer_addr

    def set_wallet_pkey(self, wallet_pkey: str):
        self._wallet_pkey = wallet_pkey

    def set_signer_pkey(self, signer_pkey: str):
        self._signer_pkey = signer_pkey

    def get_api_key(self) -> BSXApiKey:
        try:
            self._rwLock.acquire_read()
            return self._api_key
        finally:
            self._rwLock.release_read()

    def get_wallet_address(self):
        return self._wallet_addr

    def get_wallet_key(self):
        return self._wallet_pkey

    def get_signer_key(self):
        return self._signer_pkey
