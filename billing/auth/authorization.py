from typing import Any, Optional

from aiohttp_security import AbstractAuthorizationPolicy

from billing.db import queries
from billing.db.wrapper import Database
from billing.structs import User


class DbAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, db: Database) -> None:
        self.db = db

    async def authorized_userid(self, identity: str) -> Optional[str]:
        query = queries.get_user_by_username(identity)
        row = await self.db.one(query)

        if row is None:
            return None

        user = User(**row)
        userid = user.id

        return userid

    async def permits(
            self,
            identity: str,
            permission: str,
            context: Optional[Any] = None,
    ) -> bool:
        return True
