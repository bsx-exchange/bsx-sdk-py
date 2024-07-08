from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

import pandas

from .base import DataClassMeta, Paging


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

    @staticmethod
    def from_str(value: str) -> 'Side':
        if value is None:
            return None

        if value.upper() == "BUY":
            return Side.BUY
        elif value.upper() == "SELL":
            return Side.SELL

        return None


class OrderType(Enum):
    LIMIT = 0
    MARKET = 1
    STOP = 2

    @staticmethod
    def from_str(value: int) -> 'OrderType':
        if value is None:
            return None

        if value == OrderType.LIMIT:
            return OrderType.LIMIT
        elif value == OrderType.MARKET:
            return OrderType.MARKET
        elif value == OrderType.STOP:
            return OrderType.STOP

        return None


class OrderStatus(Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    DONE = "DONE"

    @staticmethod
    def from_str(value: str) -> 'OrderStatus':
        if value is None:
            return None

        if value.upper() == "PENDING":
            return OrderStatus.PENDING
        elif value.upper() == "OPEN":
            return OrderStatus.OPEN
        elif value.upper() == "DONE":
            return OrderStatus.DONE

        return None


class TransferType(Enum):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"

    @staticmethod
    def from_str(value: str) -> 'TransferType':
        if value is None:
            return None

        if value.upper() == "WITHDRAW":
            return TransferType.WITHDRAW
        elif value.upper() == "DEPOSIT":
            return TransferType.DEPOSIT

        return None


@dataclass
class CreateOrderParams(metaclass=DataClassMeta):
    """
    Contains parameters required for creating a new order

    Args:
        side (Side): The side of the order

        type (OrderType): The type of order

        product_index (int): Product to place order on. (BTC-PERP=1, ETH-PERP=2, SOL-PERP=3)

        price (Decimal): The max or min price limit to buy or sell at

        size (Decimal): The amount to buy or sell

        time_in_force (str): GTC | IOC | FOK. default is GTC

        nonce (int): timestamp in nanosecond that is larger than (request received time  - 10 minutes)

        post_only (bool): optional; default is false

        reduce_only (bool): optional; default is false

        client_order_id (str): optional; default is None. Max 32 alphabet characters. Case-insensitive. Must be unique among all open orders of the current user
    """
    side: Side
    type: OrderType
    product_index: int
    price: Decimal
    size: Decimal
    time_in_force: str
    nonce: int
    post_only: bool = False
    reduce_only: bool = False
    client_order_id: Optional[str] = None


@dataclass
class Trade(metaclass=DataClassMeta):
    id: str
    price: Decimal
    size: Decimal
    liquidity_indicator: str
    time: datetime
    funding_payment: Decimal
    trading_fee: Decimal
    sequencer_fee: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'Trade':
        return Trade(
            id=str(data["id"]) if "id" in data else None,
            price=Decimal(data["price"]) if "price" in data else None,
            size=Decimal(data["size"]) if "size" in data else None,
            liquidity_indicator=data["liquidity_indicator"] if "liquidity_indicator" in data else None,
            time=pandas.Timestamp(int(data['time'])) if 'time' in data else None,
            funding_payment=Decimal(data["funding_payment"]) if "funding_payment" in data else None,
            trading_fee=Decimal(data["trading_fee"]) if "trading_fee" in data else None,
            sequencer_fee=Decimal(data["sequencer_fee"]) if "sequencer_fee" in data else None,
        )


@dataclass
class Order(metaclass=DataClassMeta):
    """
    Contains information about an order

    Args:
        id (str): The order ID, should be an uuid

        price (Decimal): The original price (in quote unit) of the order. Example 45000.1 (USDC)

        size (Decimal): The original size (in base unit) of the order. Example 0.3 (BTC)

        product_id (str): The product of the order

        side (str): Order's side. Possible values: BUY, SELL

        type (str): Order's type. Possible values: LIMIT, MARKET, STOP

        time_in_force (str): GTC | IOC | FOK

        nonce (int): The nonce of the order

        post_only (bool): Post-only means the order will only be placed as a maker order.
        If any part of the order results in taking liquidity, the order will be rejected and no part of it will execute.

        reduce_only (bool): Indicates if the order is reduce-only

        created_at (datetime): Created at timestamp in nanosecond

        cancel_reason (str): The cancel reason (if exists). Possible values: user/admin/insufficient funds/etc

        reject_reason (str): The reason reason (if exists)

        cancel_reject_reason (str): The cancel reason reason (if exists)

        filled_fees (Decimal): The total filled fees (in quote unit - USDC) of the order

        filled_size (Decimal): The total filled size (in base unit - BTC) of the order

        status (str): PENDING | OPEN | DONE

        sender (str): The owner address of the order

        avg_price (Decimal): The average price (in quote unit - USDC) of the order

        cancel_requested (bool): Indicates if the order is cancel requested

        is_liquidation (bool): Indicates if the order is a liquidation order

        initial_margin (str): Initial Margin Requirement for the order

        client_order_id (str): The client order ID specified by user when creating new orders
    """
    id: str
    price: Decimal
    size: Decimal
    product_id: str
    side: str
    type: str
    time_in_force: str
    nonce: int
    post_only: bool
    reduce_only: bool
    created_at: datetime
    cancel_reason: str
    reject_reason: str
    cancel_reject_reason: str
    filled_fees: Decimal
    filled_size: Decimal
    status: str
    sender: str
    avg_price: Decimal
    cancel_requested: bool
    is_liquidation: bool
    initial_margin: str
    last_trades: list[Trade]
    client_order_id: str

    @staticmethod
    def from_dict(data: dict) -> 'Order':
        return Order(
            id=str(data["id"]) if "id" in data else None,
            price=Decimal(data["price"]) if "price" in data else None,
            size=Decimal(data["size"]) if "size" in data else None,
            product_id=str(data["product_id"]) if "product_id" in data else None,
            side=str(data["side"]) if "side" in data else None,
            type=str(data["type"]) if "type" in data else None,
            time_in_force=str(data["time_in_force"]) if "time_in_force" in data else None,
            nonce=int(data["nonce"]) if "nonce" in data else None,
            post_only=bool(data["post_only"]) if "post_only" in data else None,
            reduce_only=bool(data["reduce_only"]) if "reduce_only" in data else None,
            created_at=pandas.Timestamp(int(data['created_at_ts'])) if 'created_at_ts' in data else None,
            cancel_reason=str(data["cancel_reason"]) if "cancel_reason" in data else None,
            reject_reason=str(data["reject_reason"]) if "reject_reason" in data else None,
            cancel_reject_reason=str(data["cancel_reject_reason"]) if "cancel_reject_reason" in data else None,
            filled_fees=Decimal(data["filled_fees"]) if "filled_fees" in data else None,
            filled_size=Decimal(data["filled_size"]) if "filled_size" in data else None,
            status=str(data["status"]) if "status" in data else None,
            sender=str(data["sender"]) if "sender" in data else None,
            avg_price=Decimal(data["avg_price"]) if "avg_price" in data else None,
            cancel_requested=bool(data["cancel_requested"]) if "cancel_requested" in data else None,
            is_liquidation=bool(data["is_liquidation"]) if "is_liquidation" in data else None,
            initial_margin=str(data["initial_margin"]) if "initial_margin" in data else None,
            last_trades=[Trade.from_dict(i) for i in data.get("last_trades", [])],
            client_order_id=data["client_order_id"] if "client_order_id" in data else None,
        )


@dataclass
class CancelMultipleOrdersParams(metaclass=DataClassMeta):
    product_ids: Optional[list[str]] = None
    order_ids: Optional[list[str]] = None
    nonces: Optional[list[int]] = None


@dataclass
class CancelOrderResult(metaclass=DataClassMeta):
    """
    Returned if an order is cancelled successfully

    Args:
        order_id (str): Order id of the cancelled order

        nonce (int): Nonce of the cancelled order
    """
    order_id: str
    nonce: int
    client_order_id: str

    @staticmethod
    def from_dict(data: dict) -> 'CancelOrderResult':
        return CancelOrderResult(
            order_id=str(data["order_id"]) if "order_id" in data else None,
            nonce=data["nonce"] if "nonce" in data else None,
            client_order_id=data["client_order_id"] if "client_order_id" in data else None,
        )


@dataclass
class CancelMultipleOrdersResult(metaclass=DataClassMeta):
    cancelled_orders: list[CancelOrderResult]

    @staticmethod
    def from_dict(data: dict) -> 'CancelMultipleOrdersResult':
        return CancelMultipleOrdersResult(
            cancelled_orders=[CancelOrderResult.from_dict(i) for i in
                              data["cancelled_orders"]] if "cancelled_orders" in data else []
        )


@dataclass
class OrderListingResult(metaclass=DataClassMeta):
    orders: list[Order]

    @staticmethod
    def from_dict(data: dict) -> 'OrderListingResult':
        return OrderListingResult(
            orders=[Order.from_dict(i) for i in data["orders"]] if "orders" in data else []
        )


@dataclass
class GetOrderHistoryParams:
    product_id: str = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = 100
    statuses: list[OrderStatus] = None
    client_order_ids: list[str] = None


@dataclass
class CancelOrderParams:
    order_id: Optional[str] = None
    nonce: Optional[str] = None
    client_order_id: Optional[str] = None


@dataclass
class CancelOrdersParams:
    order_ids: list[str] = None
    nonces: list[str] = None
    client_order_ids: list[str] = None


@dataclass
class CancelAllParams:
    product_id: str


@dataclass
class BatchOrderUpdateParams:
    operations: list[CreateOrderParams | CancelOrderParams | CancelOrdersParams | CancelAllParams]


@dataclass
class BatchOrderUpdateResult:
    code: int
    message: str
    detail: Order | CancelOrderResult | CancelMultipleOrdersResult

    @staticmethod
    def from_dict(data: dict) -> 'BatchOrderUpdateResult':
        detail = None
        if data.get('create_order_response') is not None:
            detail = Order.from_dict(data['create_order_response'])
        if data.get('cancel_response') is not None:
            detail = CancelOrderResult.from_dict(data['cancel_response'])
        if data.get('cancel_orders_response') is not None:
            detail = CancelMultipleOrdersResult.from_dict(data['cancel_orders_response'])
        return BatchOrderUpdateResult(
            code=data['code'] if 'code' in data else None,
            message=data['message'] if 'message' in data else '',
            detail=detail
        )


@dataclass
class BatchOrderUpdateResponse:
    data: list[BatchOrderUpdateResult]

    @staticmethod
    def from_dict(data: dict) -> 'BatchOrderUpdateResponse':
        items = []
        for item in data['data']:
            items.append(BatchOrderUpdateResult.from_dict(item))

        return BatchOrderUpdateResponse(data=items)


@dataclass
class GetTradeHistoryParams:
    product_id: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    page: int = 1
    limit: int = 100


@dataclass
class GetTradeHistoryResponse:
    product_id: str
    wallet_address: str
    trades: list[Trade]
    page: int
    total: int

    @staticmethod
    def from_dict(data: dict) -> 'GetTradeHistoryResponse':
        return GetTradeHistoryResponse(
            product_id=data['product_id'] if 'product_id' in data else None,
            wallet_address=data['wallet_address'] if 'wallet_address' in data else None,
            trades=[Trade.from_dict(t) for t in data['trades']] if 'trades' in data else None,
            page=data['page'] if 'page' in data else None,
            total=data['total'] if 'total' in data else None,
        )


@dataclass
class PerpetualProductConfig:
    initial_margin: Decimal
    maintenance_margin: Decimal
    max_leverage: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'PerpetualProductConfig':
        return PerpetualProductConfig(
            initial_margin=Decimal(data["initial_margin"]) if "initial_margin" in data else None,
            maintenance_margin=Decimal(data["maintenance_margin"]) if "maintenance_margin" in data else None,
            max_leverage=Decimal(data["max_leverage"]) if "max_leverage" in data else None
        )


@dataclass
class Product:
    index: int
    product_id: str
    base_asset_symbol: str
    quote_asset_symbol: str
    underlying: str
    display_name: str
    display_base_asset_symbol: str
    enabled: bool
    post_only: bool
    base_increment: Decimal
    quote_increment: Decimal
    quote_volume_24h: Decimal
    change_24h: Decimal
    high_24h: Decimal
    low_24h: Decimal
    last_price: Decimal
    mark_price: Decimal
    index_price: Decimal
    max_position_size: Decimal
    open_interest: Decimal
    funding_interval: Decimal
    next_funding_rate: Decimal
    next_funding_time: Decimal
    last_cumulative_funding: Decimal
    min_order_size: Decimal
    predicted_funding_rate: Decimal
    perpetual_product_config: PerpetualProductConfig

    @staticmethod
    def from_dict(data: dict) -> "Product":
        return Product(
            index=int(data['index']) if 'index' in data else None,
            product_id=data['product_id'] if 'product_id' in data else None,
            base_asset_symbol=data['base_asset_symbol'] if 'base_asset_symbol' in data else None,
            quote_asset_symbol=data['quote_asset_symbol'] if 'quote_asset_symbol' in data else None,
            underlying=data['underlying'] if 'underlying' in data else None,
            display_name=data['display_name'] if 'display_name' in data else None,
            display_base_asset_symbol=data[
                'display_base_asset_symbol'] if 'display_base_asset_symbol' in data else None,
            enabled=data['enabled'] if 'enabled' in data else None,
            post_only=data['post_only'] if 'post_only' in data else None,
            base_increment=Decimal(data['base_increment']) if 'base_increment' in data else None,
            quote_increment=Decimal(data['quote_increment']) if 'quote_increment' in data else None,
            quote_volume_24h=Decimal(data['quote_volume_24h']) if 'quote_volume_24h' in data else None,
            change_24h=Decimal(data['change_24h']) if 'change_24h' in data else None,
            high_24h=Decimal(data['high_24h']) if 'high_24h' in data else None,
            low_24h=Decimal(data['low_24h']) if 'low_24h' in data else None,
            last_price=Decimal(data['last_price']) if 'last_price' in data else None,
            mark_price=Decimal(data['mark_price']) if 'mark_price' in data else None,
            index_price=Decimal(data['index_price']) if 'index_price' in data else None,
            max_position_size=Decimal(data['max_position_size']) if 'max_position_size' in data else None,
            open_interest=Decimal(data['open_interest']) if 'open_interest' in data else None,
            funding_interval=Decimal(data['funding_interval']) if 'funding_interval' in data else None,
            next_funding_rate=Decimal(data['next_funding_rate']) if 'next_funding_rate' in data else None,
            next_funding_time=Decimal(data['next_funding_time']) if 'next_funding_time' in data else None,
            last_cumulative_funding=Decimal(
                data['last_cumulative_funding']) if 'last_cumulative_funding' in data else None,
            min_order_size=Decimal(data['min_order_size']) if 'min_order_size' in data else None,
            predicted_funding_rate=Decimal(
                data['predicted_funding_rate']) if 'predicted_funding_rate' in data else None,
            perpetual_product_config=PerpetualProductConfig.from_dict(
                data['perpetual_product_config']) if 'perpetual_product_config' in data else None,
        )


@dataclass
class GetProductsResponse:
    products: list[Product]

    @staticmethod
    def from_dict(data: dict) -> 'GetProductsResponse':
        return GetProductsResponse(
            products=[Product.from_dict(p) for p in data['products']] if 'products' in data else []
        )


@dataclass
class GetFundingHistoryParams:
    product_id: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    limit: int = 20
    page: int = 1


@dataclass
class FundingRate:
    time: datetime
    rate: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'FundingRate':
        return FundingRate(
            time=pandas.Timestamp(int(data['time'])) if 'time' in data else None,
            rate=Decimal(data['rate']) if 'rate' in data else None,
        )


@dataclass
class GetFundingHistoryResponse:
    product_id: str
    items: list[FundingRate]
    paging: Paging

    @staticmethod
    def from_dict(data: dict) -> 'GetFundingHistoryResponse':
        return GetFundingHistoryResponse(
            product_id=data['product_id'] if 'product_id' in data else None,
            items=[FundingRate.from_dict(i) for i in data['items']] if 'items' in data else None,
            paging=Paging.from_dict(data['paging']) if 'paging' in data else None,
        )


@dataclass
class GetTransferHistoryParams:
    type: TransferType
    start_time: datetime
    end_time: datetime
    page: int = 1
