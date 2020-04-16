import decimal
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import insert, select
from sqlalchemy.sql import Insert, Select

from billing.db.paging import paginate
from billing.db.tables import operations
from billing.resources import OperationType
from billing.typings import Order

everything = [
    operations.c.id,
    operations.c.wallet_id,
    operations.c.source_wallet_id,
    operations.c.destination_wallet_id,
    operations.c.type,
    operations.c.amount,
    operations.c.timestamp,
]


def get_operations_by_wallet_id(
        wallet_id: str,
        timestamp: Optional[datetime],
        order: Order,
        limit: int,
) -> Select:
    query = select(everything).where(operations.c.wallet_id == wallet_id)
    query = paginate(query, {operations.c.timestamp: timestamp}, order, limit)

    return query


def get_operations_amounts_by_wallet_id(wallet_id: str) -> Select:
    return select([operations.c.amount]).where(
        operations.c.wallet_id == wallet_id
    )


def create_operation_deposit(
        wallet_id: str,
        amount: decimal.Decimal,
) -> Insert:
    return insert(operations).values(
        wallet_id=wallet_id,
        source_wallet_id=None,
        destination_wallet_id=wallet_id,
        type=OperationType.DEPOSIT,
        amount=amount,
        timestamp=datetime.now(),
    ).returning(*everything)


def create_operation_transfer(
        source_wallet_id: str,
        destination_wallet_id: str,
        amount: decimal.Decimal,
) -> Insert:
    operation: Dict[str, Any] = {
        'wallet_id': None,
        'source_wallet_id': source_wallet_id,
        'destination_wallet_id': destination_wallet_id,
        'type': OperationType.TRANSFER,
        'amount': None,
        'timestamp': datetime.now(),
    }

    # WTF: Create a couple of operations per each wallet for simple `SELECT`
    # without `OR` clause.
    return insert(operations).values(
        [
            {
                **operation,
                **{
                    'wallet_id': source_wallet_id,
                    'amount': -amount,
                },
            },
            {
                **operation,
                **{
                    'wallet_id': destination_wallet_id,
                    'amount': +amount,
                },
            },
        ],
    ).returning(*everything)
