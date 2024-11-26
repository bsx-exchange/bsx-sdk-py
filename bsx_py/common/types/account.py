from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
import pandas

from bsx_py.common.types.market import StopPriceOption


class CollateralMode(str, Enum):
    MULTI_COLLATERAL = "MULTI_COLLATERAL"
    USDC_COLLATERAL = "USDC_COLLATERAL"

    @staticmethod
    def from_str(value: str) -> "CollateralMode":
        if value is None:
            return None
        value = value.upper()
        if value == "MULTI_COLLATERAL":
            return CollateralMode.MULTI_COLLATERAL
        elif value == "USDC_COLLATERAL":
            return CollateralMode.USDC_COLLATERAL
        return None


class MarginMode(str, Enum):
    CROSS = "CROSS"
    ISOLATED = "ISOLATED"

    @staticmethod
    def from_str(value: str) -> "MarginMode":
        if value is None:
            return None
        value = value.upper()
        if value == "CROSS":
            return MarginMode.CROSS
        elif value == "ISOLATED":
            return MarginMode.ISOLATED
        return None


@dataclass
class WithdrawParams:
    """
    Contains parameters for creating a withdrawal request

    Args:
        amount (Decimal): Token amount to withdraw. For USDC, the minimum amount is 2 USDC.
        We currently only allow withdraw up to min(settled_usdc_balance, free_collateral).

        nonce (int): timestamp in nanosecond that is larger than (request received time  - 10 minutes)
    """
    amount: Decimal
    nonce: int


@dataclass
class TokenBalance:
    address: str
    balance: Decimal

    @staticmethod
    def from_dict(data: dict) -> "TokenBalance":
        return TokenBalance(address=data["address"], balance=Decimal(data.get("balance", "0")))


@dataclass
class StopPriceLevel:
    price: Decimal
    size: Decimal
    stop_price_option: StopPriceOption

    @staticmethod
    def from_dict(data: dict) -> "StopPriceLevel":
        if data is None:
            return None
        return StopPriceLevel(
            price=Decimal(data["price"]) if "price" in data else None,
            size=Decimal(data["size"]) if "size" in data else None,
            stop_price_option=StopPriceOption.from_str(data["stop_price_option"])
        )


@dataclass
class StopPosition:
    nearest_take_profit: StopPriceLevel
    nearest_stop_loss: StopPriceLevel

    @staticmethod
    def from_dict(data: dict) -> "StopPosition":
        return StopPosition(
            nearest_take_profit=StopPriceLevel.from_dict(data["nearest_take_profit"]) if "nearest_take_profit" in data else None,
            nearest_stop_loss=StopPriceLevel.from_dict(data["nearest_stop_loss"]) if "nearest_stop_loss" in data else None
        )


@dataclass
class PortfolioSummary:
    collateral_mode: CollateralMode
    collateral_margin_balance: Decimal
    cross_margin_balance: Decimal
    margin_usage: Decimal
    account_leverage: Decimal
    in_liquidation: bool
    free_collateral: Decimal
    total_account_value: Decimal
    total_notional: Decimal
    usdc_balance: Decimal
    unsettled_usdc: Decimal
    realized_pnl: Decimal
    total_initial_margin: Decimal
    total_maintenance_margin: Decimal
    token_balances: list[TokenBalance]
    has_pending_withdrawal: bool
    total_unrealized_pnl: Decimal
    total_collateral_value: Decimal
    margin_health: Decimal
    has_pending_swap: Decimal
    total_isolated_order_reserve: Decimal

    @staticmethod
    def from_dict(data: dict) -> "PortfolioSummary":
        return PortfolioSummary(
            collateral_mode=CollateralMode.from_str(data["collateral_mode"]),
            collateral_margin_balance=Decimal(data.get("collateral_margin_balance", "0")),
            cross_margin_balance=Decimal(data.get("cross_margin_balance", "0")),
            margin_usage=Decimal(data.get("margin_usage", "0")),
            account_leverage=Decimal(data.get("account_leverage", "0")),
            in_liquidation=bool(data.get("in_liquidation", False)),
            free_collateral=Decimal(data.get("free_collateral", "0")),
            total_account_value=Decimal(data.get("total_account_value", "0")),
            total_notional=Decimal(data.get("total_notional", "0")),
            usdc_balance=Decimal(data.get("usdc_balance", "0")),
            unsettled_usdc=Decimal(data.get("unsettled_usdc", "0")),
            realized_pnl=Decimal(data.get("realized_pnl", "0")),
            total_initial_margin=Decimal(data.get("total_initial_margin", "0")),
            total_maintenance_margin=Decimal(data.get("total_maintenance_margin", "0")),
            token_balances=[TokenBalance.from_dict(token_balance) for token_balance in data.get("token_balances", [])],
            has_pending_withdrawal=bool(data["has_pending_withdrawal"]) if "has_pending_withdrawal" in data else None,
            total_unrealized_pnl=Decimal(data.get("total_unrealized_pnl", "0")),
            total_collateral_value=Decimal(data.get("total_collateral_value", "0")),
            margin_health=Decimal(data.get("margin_health", "0")),
            has_pending_swap=bool(data["has_pending_swap"]) if "has_pending_swap" in data else None,
            total_isolated_order_reserve=Decimal(data.get("total_isolated_order_reserve", "0")),
        )


@dataclass
class Position:
    product_index: int
    product_id: str
    margin_mode: MarginMode
    margin_balance: Decimal
    net_size: Decimal
    avg_entry_price: Decimal
    initial_margin_requirement: Decimal
    maintenance_margin_requirement: Decimal
    liquidation_price: Decimal
    unrealized_pnl: Decimal
    mark_price: Decimal
    leverage: Decimal
    unsettled_funding: Decimal
    funding_index: Decimal
    quote_balance: Decimal
    stop_position: StopPosition
    index_price: Decimal
    isolated_usdc_balance: Decimal
    in_isolated_liquidation: bool
    free_isolated_usdc_balance: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'Position':
        return Position(
            product_index=int(data["product_index"]) if "product_index" in data else None,
            product_id=str(data["product_id"]) if "product_id" in data else None,
            margin_mode=MarginMode.from_str(data["margin_mode"]),
            margin_balance=Decimal(data.get("margin_balance", "0")),
            net_size=Decimal(data.get("net_size", "0")),
            avg_entry_price=Decimal(data.get("avg_entry_price", "0")),
            initial_margin_requirement=Decimal(data.get("initial_margin_requirement", "0")),
            maintenance_margin_requirement=Decimal(data.get("maintenance_margin_requirement", "0")),
            liquidation_price=Decimal(data.get("liquidation_price", "0")),
            unrealized_pnl=Decimal(data.get("unrealized_pnl", "0")),
            mark_price=Decimal(data["mark_price"]) if "mark_price" in data else None,
            leverage=Decimal(data["leverage"]) if "leverage" in data else None,
            unsettled_funding=Decimal(data["unsettled_funding"]) if "unsettled_funding" in data else None,
            funding_index=Decimal(data.get("funding_index", "0")),
            quote_balance=Decimal(data.get("quote_balance", "0")),
            stop_position=StopPosition.from_dict(data["stop_position"]) if "stop_position" in data else None,
            index_price=Decimal(data["index_price"]) if "index_price" in data else None,
            isolated_usdc_balance=Decimal(data.get("isolated_usdc_balance", "0")),
            in_isolated_liquidation=bool(data.get("in_isolated_liquidation", False)),
            free_isolated_usdc_balance=Decimal(data.get("free_isolated_usdc_balance", "0")),
        )


@dataclass
class OrderStats:
    total_orders: Decimal
    total_done_orders: Decimal
    total_open_orders: Decimal
    total_pending_orders: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'OrderStats':
        return OrderStats(
            total_orders=Decimal(data["total_orders"]) if "total_orders" in data else None,
            total_done_orders=Decimal(data["total_done_orders"]) if "total_done_orders" in data else None,
            total_open_orders=Decimal(data["total_open_orders"]) if "total_open_orders" in data else None,
            total_pending_orders=Decimal(data["total_pending_orders"]) if "total_pending_orders" in data else None,
        )


@dataclass
class ProductStats:
    total_orders: Decimal
    total_done_orders: Decimal
    total_open_orders: Decimal
    total_pending_orders: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'ProductStats':
        return ProductStats(
            total_orders=Decimal(data["total_orders"]) if "total_orders" in data else None,
            total_done_orders=Decimal(data["total_done_orders"]) if "total_done_orders" in data else None,
            total_open_orders=Decimal(data["total_open_orders"]) if "total_open_orders" in data else None,
            total_pending_orders=Decimal(data["total_pending_orders"]) if "total_pending_orders" in data else None,
        )


@dataclass
class PortfolioProduct:
    product_id: str
    stat: ProductStats

    @staticmethod
    def from_dict(data: dict) -> 'PortfolioProduct':
        return PortfolioProduct(
            product_id=data.get("product_id"),
            stat=ProductStats.from_dict(data.get('stat', {}))
        )


@dataclass
class TradingStats:
    total_trading_volume: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'TradingStats':
        return TradingStats(
            total_trading_volume=Decimal(data['total_trading_volume']) if "total_trading_volume" in data else None
        )


@dataclass
class TokenStat:
    address: str
    total_deposit: Decimal
    total_withdraw: Decimal

    def from_dict(data: dict) -> 'TokenStat':
        return TokenStat(
            address=data["address"],
            total_deposit=Decimal(data.get("total_deposit", "0")),
            total_withdraw=Decimal(data.get("total_withdraw", "0"))
        )


@dataclass
class PortfolioStats:
    order_stats: OrderStats
    products: list[PortfolioProduct]
    trading_stats: TradingStats
    tokens: list[TokenStat]
    total_deposit: Decimal
    total_withdraw: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'PortfolioStats':
        return PortfolioStats(
            order_stats=OrderStats.from_dict(data.get('order_stats', {})),
            products=[PortfolioProduct.from_dict(i) for i in data.get('products', [])],
            trading_stats=TradingStats.from_dict(data.get('trading_stats', {})),
            tokens=[TokenStat.from_dict(i) for i in data.get("tokens", [])],
            total_deposit=Decimal(data["total_deposit"]) if "total_deposit" in data else None,
            total_withdraw=Decimal(data["total_withdraw"]) if "total_withdraw" in data else None
        )


@dataclass
class Portfolio:
    account: str
    summary: PortfolioSummary
    positions: list[Position]
    stats: PortfolioStats
    maker_fee: float
    taker_fee: float

    @staticmethod
    def from_dict(data: dict):
        return Portfolio(
            account=data["account"],
            summary=PortfolioSummary.from_dict(data["summary"]) if "summary" in data else None,
            positions=[Position.from_dict(i) for i in data.get("positions", [])],
            stats=PortfolioStats.from_dict(data["stats"]) if "stats" in data else None,
            maker_fee=data["maker_fee"],
            taker_fee=data["taker_fee"]
        )


@dataclass
class APIKey:
    api_key: str
    api_secret: str
    created_at: datetime
    updated_at: datetime
    name: str
    sender: str
    signer: str

    @staticmethod
    def from_dict(data: dict) -> "APIKey":
        return APIKey(
            api_key=data['api_key'] if 'api_key' in data else None,
            api_secret=data['api_secret'] if 'api_secret' in data else None,
            name=data['name'] if 'name' in data else None,
            sender=data['sender'] if 'sender' in data else None,
            signer=data['signer'] if 'signer' in data else None,
            created_at=pandas.Timestamp(int(data['created_at'])) if 'created_at' in data else None,
            updated_at=pandas.Timestamp(int(data['updated_at'])) if 'updated_at' in data else None,
        )


@dataclass
class GetAPIKeysResponse:
    api_keys: list[APIKey]

    @staticmethod
    def from_dict(data: dict) -> "GetAPIKeysResponse":
        return GetAPIKeysResponse(
            api_keys=[APIKey.from_dict(i) for i in data['api_keys']] if 'api_keys' in data else None,
        )
