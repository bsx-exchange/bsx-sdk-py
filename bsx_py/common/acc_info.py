from abc import ABCMeta, abstractmethod

from bsx_py.common.types.auth import BSXApiKey


class AccountInfo(metaclass=ABCMeta):
    @abstractmethod
    def get_api_key(self) -> BSXApiKey:
        raise NotImplementedError

    @abstractmethod
    def get_wallet_address(self):
        raise NotImplementedError

    @abstractmethod
    def get_wallet_key(self):
        raise NotImplementedError

    @abstractmethod
    def get_signer_key(self):
        raise NotImplementedError
