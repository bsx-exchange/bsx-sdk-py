import functools
from enum import Enum

import requests
from eip712_structs import make_domain
from eth_account.signers.local import LocalAccount

from bsx_py.client.rest.account.client import AccountClient
from bsx_py.client.rest.market.client import MarketClient
from bsx_py.common.exception import UnauthenticatedException, NotSupportOperationException, \
    WalletPrivateNotProvidedException
from bsx_py.common.types.account import WithdrawParams, Portfolio, GetAPIKeysResponse, APIKey
from bsx_py.common.types.market import *
from bsx_py.helper import AccountManager


def _refresh_api_key_if_needed(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._check_and_renew_api_key_if_needed()
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

    @staticmethod
    def from_api_key(api_key: str, api_secret: str, signer: LocalAccount, env: Environment | str) -> 'BSXInstance':
        """
        Initialize a new BSXInstance object using an active API key.

        The BSXInstance returned by this method will not be able to submit withdrawal requests

        Attributes:
            api_key (str): BSX API key

            api_secret (str): BSX secret

            signer (LocalAccount): signer wallet used to sign requests

            env (Environment|str): environment to use (Testnet or mainnet) or the domain in plain text

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        instance = BSXInstance.__new__(BSXInstance)
        domain = env.value if isinstance(env, Environment) else env
        config = instance._get_chain_config(domain)
        eip712_domain = instance._build_eip712_domain(config)

        instance._acc_manager = AccountManager.from_api_key(api_key, api_secret, signer.key, domain, eip712_domain)
        instance._account_client = AccountClient(
            domain=domain, domain_signature=eip712_domain, config=config, acc_info=instance._acc_manager
        )
        instance._market_client = MarketClient(
            domain=domain, domain_signature=eip712_domain, acc_info=instance._acc_manager
        )

        return instance

    def __init__(self, env: Environment | str, wallet: LocalAccount, signer: LocalAccount):
        """
        Initialize a new BSXInstance object using main wallet's private key

        Attributes:
            env (Environment|str): environment to use (Testnet or mainnet) or the domain in plain text

            wallet (LocalAccount): main wallet

            signer (LocalAccount): signer wallet used to sign requests

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        domain = env.value if isinstance(env, Environment) else env
        config = self._get_chain_config(domain)
        eip712_domain = self._build_eip712_domain(config)

        self._acc_manager = AccountManager.from_secret(wallet.key, signer.key, domain, eip712_domain)
        self._account_client = AccountClient(
            domain=domain, domain_signature=eip712_domain, config=config, acc_info=self._acc_manager
        )
        self._market_client = MarketClient(
            domain=domain, domain_signature=eip712_domain, acc_info=self._acc_manager
        )

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
        """
        Submit withdrawal request

        Attributes:
            params (WithdrawParams): parameters to create withdrawal request

        Return:
            bool: whether the withdrawal request was created successfully or not

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        try:
            return self._account_client.submit_withdrawal_request(params)
        except WalletPrivateNotProvidedException:
            raise NotSupportOperationException("BSXInstance created by API key cannot submit withdrawal request")

    @_refresh_api_key_if_needed
    def get_portfolio_detail(self) -> Portfolio:
        """
        Get portfolio detail

        Return:
            Portfolio: portfolio detail of the current user

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._account_client.get_portfolio_detail()

    @_refresh_api_key_if_needed
    def batch_update_orders(self, params: BatchOrderUpdateParams) -> BatchOrderUpdateResponse:
        """
        Update orders in batch

        Attributes:
            params (BatchOrderUpdateParams): update orders parameters

        Return:
            BatchOrderUpdateResponse: update result. The order of items in the result is the same as the order of items in the input params

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.batch_update_orders(params=params)

    @_refresh_api_key_if_needed
    def get_user_trade_history(self, params: GetTradeHistoryParams) -> GetTradeHistoryResponse:
        """
        Get user's trade history

        Attributes:
            params (GetTradeHistoryParams): filter parameters

        Return:
            GetTradeHistoryResponse: trade history

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.get_user_trade_history(params=params)

    @_refresh_api_key_if_needed
    def get_products(self) -> list[Product]:
        """
        Get all markets

        Return:
            list[Product]: list of all markets

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.get_products().products

    @_refresh_api_key_if_needed
    def get_funding_history(self, params: GetFundingHistoryParams) -> GetFundingHistoryResponse:
        """
        Get funding rate history

        Attributes:
            params (GetFundingHistoryParams): filter parameters

        Return:
            GetFundingHistoryResponse: funding rate history

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.get_funding_history(params=params)

    @_refresh_api_key_if_needed
    def get_api_key_list(self) -> GetAPIKeysResponse:
        """
        Get all active API keys

        Return:
            GetAPIKeysResponse: API keys list

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._account_client.get_api_key_list()

    def delete_user_api_key(self, api_key: str) -> str:
        """
        Delete an API key

        Attributes:
            api_key (str): API key to be deleted

        Return:
            str: API key that was deleted

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._account_client.delete_user_api_key(api_key)

    def create_user_api_key(self, name: str = "") -> APIKey:
        """
        Create a new API key

        Attributes:
            name (str): name of the new API key

        Return:
            APIKey: new API key info

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._account_client.create_user_api_key(name)

    @_refresh_api_key_if_needed
    def get_products(self) -> GetProductsResponse:
        """
        Get product configs

        Return:
            GetProductsResponse: product configs

        Raises:
            BSXRequestException: If the response status is not "success".
        """
        return self._market_client.get_products()

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
        self._acc_manager.renew_api_key()

    def _check_and_renew_api_key_if_needed(self):
        self._acc_manager.check_and_renew_api_key()
