from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

import pandas

from .base import DataClassMeta


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


@dataclass
class Trade(metaclass=DataClassMeta):
    id: str
    price: Decimal
    size: Decimal
    liquidity_indicator: int
    time: str
    funding_payment: str
    trading_fee: Decimal
    sequencer_fee: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'Trade':
        return Trade(
            id=str(data["id"]) if "id" in data else None,
            price=Decimal(data["price"]) if "price" in data else None,
            size=Decimal(data["size"]) if "size" in data else None,
            liquidity_indicator=int(data["liquidity_indicator"]) if "liquidity_indicator" in data else None,
            time=str(data["time"]) if "time" in data else None,
            funding_payment=str(data["funding_payment"]) if "funding_payment" in data else None,
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

    @staticmethod
    def from_dict(data: dict) -> 'CancelOrderResult':
        return CancelOrderResult(
            order_id=str(data["order_id"]) if "order_id" in data else None,
            nonce=data["nonce"] if "nonce" in data else None,
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
