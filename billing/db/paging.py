from operator import ge, le
from typing import Any, Callable, Dict

from sqlalchemy import Column, asc, desc
from sqlalchemy.sql import Select

from billing.typings import Order


def paginate(
        query: Select,
        columns: Dict[Column, Any],
        order: Order,
        limit: int,
) -> Select:
    orderer = get_orderer(order)
    comparator = get_comparator(order)

    for column, value in columns.items():
        query = query.order_by(orderer(column))

        if value is not None:
            query = query.where(comparator(column, value))

    return query.limit(limit)


def get_orderer(direction: Order) -> Callable[[Column], None]:
    if direction == "asc":
        return asc

    return desc


def get_comparator(direction: Order) -> Callable[[Any, Any], bool]:
    if direction == "asc":
        return ge

    return le
