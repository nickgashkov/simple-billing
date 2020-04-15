import decimal
from typing import Any, Dict, NamedTuple


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
    source_wallet_id: str
    destination_wallet_id: str
    type: str
    amount: decimal.Decimal
    timestamp: int

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_wallet_id": self.source_wallet_id,
            "destination_wallet_id": self.destination_wallet_id,
            "type": self.type,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }
