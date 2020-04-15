from sqlalchemy import insert, select
from sqlalchemy.sql import Insert, Select

from billing.db.tables import users


def get_user_by_username(username: str) -> Select:
    return select(
        [
            users.c.id,
            users.c.username,
            users.c.password,
        ]
    ).where(users.c.username == username)


def create_user(username: str, hashed_password: str) -> Insert:
    return insert(users).values(username=username, password=hashed_password)
