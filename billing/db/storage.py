import decimal
import functools
import operator
from datetime import datetime
from typing import List, Optional

from billing.auth.authentication import hash_password
from billing.db import queries
from billing.db.wrapper import Database
from billing.structs import Operation, User, Wallet
from billing.typings import Order


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


async def get_operations(
        db: Database,
        wallet_id: str,
        timestamp: Optional[datetime],
        order: Order,
        limit: int,
) -> List[Operation]:
    query = queries.get_operations_by_wallet_id(
        wallet_id,
        timestamp,
        order,
        limit,
    )
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


async def create_operation_deposit(
        db: Database,
        wallet_id: str,
        amount: decimal.Decimal,
) -> Operation:
    query = queries.create_operation_deposit(wallet_id, amount)
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
    source_operations_query = queries.get_operations_amounts_by_wallet_id(
        source_wallet_id
    )
    create_transfer_query = queries.create_operation_transfer(
        source_wallet_id,
        destination_wallet_id,
        amount,
    )

    async with db.engine.acquire() as conn:
        async with conn.begin():
            ops = await db.all(source_operations_query, conn)
            balance = functools.reduce(
                operator.add,
                (op['amount'] for op in ops),
                decimal.Decimal('0.00')
            )

            if balance < amount:
                raise RuntimeError("Insufficient funds for user")

            rows = await db.all(create_transfer_query, conn)

    return [Operation(**row) for row in rows]
