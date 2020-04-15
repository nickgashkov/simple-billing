from typing import Optional

from billing.auth.authentication import hash_password
from billing.db import queries
from billing.db.wrapper import Database
from billing.structs import User


async def get_user(db: Database, username: str) -> Optional[User]:
    query = queries.get_user_by_username(username)
    row = await db.one(query)

    if row is None:
        return None

    return User(**row)


async def create_user(db: Database, username: str, password: str) -> None:
    query = queries.create_user(username, hash_password(password))
    await db.execute(query)
