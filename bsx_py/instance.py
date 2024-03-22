import functools
from enum import Enum

import requests
from eip712_structs import make_domain
from eth_account.signers.local import LocalAccount

from bsx_py.client.rest.account.client import AccountClient, RegistrationClient
from bsx_py.client.rest.market.client import MarketClient
from bsx_py.common.exception import UnauthenticatedException
from bsx_py.common.types.account import RegisterParams, WithdrawParams, Portfolio
from bsx_py.common.types.market import CreateOrderParams, CancelOrderResult, CancelMultipleOrdersParams, \
    CancelMultipleOrdersResult, OrderListingResult, Order, GetOrderHistoryParams
from bsx_py.common.utils import AccountStorage


def _refresh_api_key_if_needed(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except UnauthenticatedException:
            self._refresh_api_key()
            return method(self, *args, **kwargs)
    return wrapper


class Environment(Enum):
    TESTNET = "https://api.testnet.bsx.exchange"
    MAINNET = "https://api.bsx.exchange"


class BSXInstance:
    """The client interface to interact with BSX Exchange

    BSXInstance will handle signing, authenticating, API key renewal internally.

    Each BSXInstance works with only one wallet. If you want to use multiple wallets, just create multiple instances.
    """

    def __init__(self, env: Environment, wallet: LocalAccount, signer: LocalAccount):
        """
        Initialize a new BSXInstance object

        Attributes:
            env (Environment): environment to use (Testnet or mainnet)

            wallet (LocalAccount): main wallet

            signer (LocalAccount): signer wallet used to sign requests

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        domain = env.value
        config = self._get_chain_config(domain)
        eip712_domain = self._build_eip712_domain(config)

        self._registration_client = RegistrationClient(domain, eip712_domain)
        api_key = self._registration_client.register(
            RegisterParams(wallet_pkey=wallet.key, signer_pkey=signer.key, message="")
        )

        self._acc_storage = AccountStorage()
        self._acc_storage.set_signer(signer)
        self._acc_storage.set_wallet(wallet)
        self._acc_storage.set_api_key(api_key)

        self._account_client = AccountClient(domain=domain, domain_signature=eip712_domain, config=config,
                                             acc_storage=self._acc_storage)
        self._market_client = MarketClient(domain=domain, domain_signature=eip712_domain, acc_storage=self._acc_storage)

    @_refresh_api_key_if_needed
    def create_order(self, params: CreateOrderParams) -> Order:
        """
        Create a new order

        Attributes:
            params (CreateOrderParams): object that contains data required to create an order

        Return:
            Order: created order

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.create_order(params)

    @_refresh_api_key_if_needed
    def cancel_order(self, order_id: str) -> CancelOrderResult:
        """
        Cancel an order by id

        Attributes:
            order_id (str): order_id that need to be cancelled

        Return:
            CancelOrderResult: cancel result

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.cancel_order(order_id=order_id)

    @_refresh_api_key_if_needed
    def cancel_bulk_orders(self, order_ids: list[str]) -> CancelMultipleOrdersResult:
        """
        Cancel multiple orders by ids

        Attributes:
            order_ids (list[str]): order_ids that need to be cancelled

        Return:
            CancelMultipleOrdersResult: cancel result

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.cancel_orders(CancelMultipleOrdersParams(order_ids=order_ids))

    @_refresh_api_key_if_needed
    def cancel_all_orders(self, product_id: str) -> CancelMultipleOrdersResult:
        """
        Cancel all open orders of a given product

        Attributes:
            product_id (str): the product that it's orders need to be cancelled

        Return:
            CancelMultipleOrdersResult: cancel result

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.cancel_all_orders(product_id)

    @_refresh_api_key_if_needed
    def get_all_open_orders(self, product_id: str) -> OrderListingResult:
        """
        Get all open orders of a given product

        Attributes:
            product_id (str): the product id

        Return:
            CancelMultipleOrdersResult: contains a list of open orders

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.get_all_open_orders(product_id)

    @_refresh_api_key_if_needed
    def get_order_history(self, params: GetOrderHistoryParams) -> OrderListingResult:
        """
        Get order history

        Attributes:
            params (GetOrderHistoryParams): parameters to get order history

        Return:
            OrderListingResult: contains a list of orders

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.get_order_history(params)

    @_refresh_api_key_if_needed
    def submit_withdrawal_request(self, params: WithdrawParams) -> bool:
        return self._account_client.submit_withdrawal_request(params)

    @_refresh_api_key_if_needed
    def get_portfolio_detail(self) -> Portfolio:
        return self._account_client.get_portfolio_detail()

    def _get_chain_config(self, domain: str):
        response = requests.get(domain + "/chain/configs")
        if response.status_code != 200:
            raise Exception(
                f"Failed to get chain config. Response code: {response.status_code}. "
                f"Response: {response.text}"
            )

        return response.json()

    def _build_eip712_domain(self, config):
        return make_domain(
            name=config["name"],
            version=config["version"],
            chainId=config["chain_id"],
            verifyingContract=config["verifying_contract"],  # note the changed naming convention here
        )

    def _refresh_api_key(self):
        acquired_write_lock = self._acc_storage.lock_all_read()

        if acquired_write_lock:
            try:
                api_key = self._registration_client.register(
                    RegisterParams(wallet_pkey=self._acc_storage.get_wallet_key(),
                                   signer_pkey=self._acc_storage.get_signer_key(), message="")
                )
                self._acc_storage.set_api_key(api_key)
            finally:
                self._acc_storage.release_all_read()
