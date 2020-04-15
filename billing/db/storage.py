import decimal
import functools
import operator
from typing import List, Optional

from billing.auth.authentication import hash_password
from billing.db import queries
from billing.db.wrapper import Database
from billing.structs import Operation, User, Wallet


async def get_user(db: Database, username: str) -> Optional[User]:
    query = queries.get_user_by_username(username)
    row = await db.one(query)

    if row is None:
        return None

    return User(**row)


async def get_wallet(db: Database, user_id: str) -> Optional[Wallet]:
    query = queries.get_wallet_by_user_id(user_id)
    row = await db.one(query)

    if row is None:
        return None

    return Wallet(**row)


async def get_wallet_balance(db: Database, wallet_id: str) -> decimal.Decimal:
    query = queries.get_operations_amounts_by_wallet_id(wallet_id)
    rows = await db.all(query)

    if not rows:
        return decimal.Decimal('0.00')

    return functools.reduce(operator.add, (row['amount'] for row in rows))


async def get_operations(db: Database, wallet_id: str) -> List[Operation]:
    query = queries.get_operations_by_wallet_id(wallet_id)
    rows = await db.all(query)

    return [Operation(**row) for row in rows]


async def create_user(db: Database, username: str, password: str) -> User:
    query = queries.create_user(username, hash_password(password))
    row = await db.one(query)

    if row is None:
        raise RuntimeError("Database didn't return user after INSERT")

    return User(**row)


async def create_wallet(db: Database, user_id: str) -> Wallet:
    query = queries.create_wallet(user_id)
    row = await db.one(query)

    if row is None:
        raise RuntimeError("Database didn't return wallet after INSERT")

    return Wallet(**row)


async def create_operation_faucet(
        db: Database,
        wallet_id: str,
        amount: decimal.Decimal,
) -> Operation:
    query = queries.create_operation_faucet(wallet_id, amount)
    row = await db.one(query)

    if row is None:
        raise RuntimeError("Database didn't return operation after INSERT")

    return Operation(**row)


async def create_operation_transfer(
        db: Database,
        source_wallet_id: str,
        destination_wallet_id: str,
        amount: decimal.Decimal,
) -> List[Operation]:
    query = queries.create_operation_transfer(
        source_wallet_id,
        destination_wallet_id,
        amount,
    )
    rows = await db.all(query)

    if not rows:
        raise RuntimeError("Database didn't return operations after INSERT")

    return [Operation(**row) for row in rows]
