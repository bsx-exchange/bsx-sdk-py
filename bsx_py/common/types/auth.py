from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class BSXApiKey:
    api_key: str
    api_secret: str
    expired_at: datetime
    name: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'BSXApiKey':
        return BSXApiKey(
            api_key=data['api_key'] if 'api_key' in data else None,
            api_secret=data['api_secret'] if 'api_secret' in data else None,
            expired_at=datetime.fromtimestamp(int(data['expired_at']) / 1e9) if 'expired_at' in data else None,
            name=data['name'] if 'name' in data else '',
        )


@dataclass
class BSXApiKeyDetail:
    api_key: str
    api_secret: str
    expired_at: datetime
    sender: str
    signer: str
    name: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'BSXApiKeyDetail':
        return BSXApiKeyDetail(
            api_key=data['api_key'] if 'api_key' in data else None,
            api_secret=data['api_secret'] if 'api_secret' in data else None,
            sender=data['sender'] if 'sender' in data else None,
            signer=data['signer'] if 'signer' in data else None,
            expired_at=datetime.fromtimestamp(int(data['expired_at']) / 1e9) if 'expired_at' in data else None,
            name=data['name'] if 'name' in data else '',
        )


@dataclass
class RegisterParams:
    wallet_pkey: str
    signer_pkey: str
    message: str
