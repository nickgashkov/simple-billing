from collections import Iterable
from typing import Any, Iterable as IterableT, Union

from sqlalchemy import Table
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DDLElement
from sqlalchemy.sql.compiler import SQLCompiler


class truncate(DDLElement):
    def __init__(self, tables: Union[Table, IterableT[Table]]) -> None:
        if not isinstance(tables, Iterable):
            tables = [tables]

        self.tables = tables


@compiles(truncate, "postgresql")
def visit_truncate(
        element: DDLElement,
        compiler: SQLCompiler,
        **kwargs: Any,
) -> str:
    return "TRUNCATE {}".format(','.join(t.name for t in element.tables))
