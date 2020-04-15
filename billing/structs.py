import datetime
import decimal
from typing import Any, Dict, NamedTuple, Optional


class User(NamedTuple):
    id: str
    username: str
    password: str

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
        }


class Wallet(NamedTuple):
    id: str
    user_id: str

    def to_json(self, balance: decimal.Decimal) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "balance": str(balance),
        }


class Operation(NamedTuple):
    id: str
    wallet_id: str
    source_wallet_id: Optional[str]
    destination_wallet_id: str
    type: str
    amount: decimal.Decimal
    timestamp: datetime.datetime

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_wallet_id": self.source_wallet_id,
            "destination_wallet_id": self.destination_wallet_id,
            "type": self.type,
            "amount": str(self.amount),
            "timestamp": self.timestamp.isoformat(),
        }
