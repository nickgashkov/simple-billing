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
