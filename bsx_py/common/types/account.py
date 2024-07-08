from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

import pandas


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
class PortfolioSummary:
    margin_use: Decimal
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
    has_pending_withdrawal: bool

    @staticmethod
    def from_dict(data: dict) -> 'PortfolioSummary':
        return PortfolioSummary(
            margin_use=Decimal(data.get("margin_use", "0")),
            account_leverage=Decimal(data.get("account_leverage", "0")),
            free_collateral=Decimal(data.get("free_collateral", "0")),
            total_account_value=Decimal(data.get("total_account_value", "0")),
            total_notional=Decimal(data.get("total_notional", "0")),
            usdc_balance=Decimal(data.get("usdc_balance", "0")),
            unsettled_usdc=Decimal(data.get("unsettled_usdc", "0")),
            realized_pnl=Decimal(data.get("realized_pnl", "0")),
            total_initial_margin=Decimal(data.get("total_initial_margin", "0")),
            total_maintenance_margin=Decimal(data.get("total_maintenance_margin", "0")),
            has_pending_withdrawal=bool(data["has_pending_withdrawal"]) if "has_pending_withdrawal" in data else None,
            in_liquidation=bool(data["in_liquidation"]) if "in_liquidation" in data else None,
        )


@dataclass
class Position:
    product_index: int
    product_id: str
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

    @staticmethod
    def from_dict(data: dict) -> 'Position':
        return Position(
            product_index=int(data["product_index"]) if "product_index" in data else None,
            product_id=str(data["product_id"]) if "product_id" in data else None,
            net_size=Decimal(data["net_size"]) if "net_size" in data else None,
            avg_entry_price=Decimal(data["avg_entry_price"]) if "avg_entry_price" in data else None,
            initial_margin_requirement=Decimal(data["initial_margin_requirement"]) if "initial_margin_requirement" in data else None,
            maintenance_margin_requirement=Decimal(data["maintenance_margin_requirement"]) if "maintenance_margin_requirement" in data else None,
            liquidation_price=Decimal(data["liquidation_price"]) if "liquidation_price" in data else None,
            unrealized_pnl=Decimal(data["unrealized_pnl"]) if "unrealized_pnl" in data else None,
            mark_price=Decimal(data["mark_price"]) if "mark_price" in data else None,
            leverage=Decimal(data["leverage"]) if "leverage" in data else None,
            unsettled_funding=Decimal(data["unsettled_funding"]) if "unsettled_funding" in data else None,
            funding_index=Decimal(data["funding_index"]) if "funding_index" in data else None,
            quote_balance=Decimal(data["quote_balance"]) if "quote_balance" in data else None,
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
class PortfolioStats:
    order_stats: OrderStats
    products: list[PortfolioProduct]
    trading_stats: TradingStats
    total_deposit: Decimal
    total_withdraw: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'PortfolioStats':
        return PortfolioStats(
            order_stats=OrderStats.from_dict(data.get('order_stats', {})),
            products=[PortfolioProduct.from_dict(i) for i in data.get('products', [])],
            trading_stats=TradingStats.from_dict(data.get('trading_stats', {})),
            total_deposit=Decimal(data["total_deposit"]) if "total_deposit" in data else None,
            total_withdraw=Decimal(data["total_withdraw"]) if "total_withdraw" in data else None
        )


@dataclass
class Portfolio:
    account: str
    summary: PortfolioSummary
    positions: list[Position]
    stats: PortfolioStats

    @staticmethod
    def from_dict(data: dict):
        return Portfolio(
            account=data["account"],
            summary=PortfolioSummary.from_dict(data["summary"]) if "summary" in data else None,
            positions=[Position.from_dict(i) for i in data.get("positions", [])],
            stats=PortfolioStats.from_dict(data["stats"]) if "stats" in data else None
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
