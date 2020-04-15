from sqlalchemy import insert, select
from sqlalchemy.sql import Insert, Select

from billing.db.tables import wallets

everything = [
    wallets.c.id,
    wallets.c.user_id,
]


def get_wallet_by_user_id(user_id: str) -> Select:
    return select(everything).where(wallets.c.user_id == user_id)


def create_wallet(user_id: str) -> Insert:
    return insert(wallets).values(user_id=user_id).returning(*everything)
