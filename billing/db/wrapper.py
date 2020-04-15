from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncContextManager,
    AsyncIterator,
    Dict,
    List,
    Optional,
)

import aiopg.sa
from aiopg.sa import SAConnection
from sqlalchemy.sql import ClauseElement

Row = Dict[str, Any]
Rows = List[Row]


class Database:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.engine: aiopg.sa.Engine = None

    async def start(self) -> None:
        self.engine = await aiopg.sa.create_engine(self.dsn)

    async def stop(self) -> None:
        if self.engine is None:
            return

        self.engine.close()
        await self.engine.wait_closed()

    async def execute(
            self,
            query: ClauseElement,
            connection: Optional[SAConnection] = None,
    ) -> None:
        async with self._get_connection(connection) as conn:
            await conn.execute(query)

    async def all(
            self,
            query: ClauseElement,
            connection: Optional[SAConnection] = None,
    ) -> Rows:
        async with self._get_connection(connection) as conn:
            cursor = await conn.execute(query)
            results = await cursor.fetchall()
        return [dict(item) for item in results]

    async def one(
            self,
            query: ClauseElement,
            connection: Optional[SAConnection] = None,
    ) -> Optional[Row]:
        async with self._get_connection(connection) as conn:
            cursor = await conn.execute(query)
            result = await cursor.fetchone()

        return dict(result) if result else None

    def _get_connection(
            self,
            conn: Optional[SAConnection]
    ) -> AsyncContextManager[SAConnection]:
        if conn is None:
            return self.engine.acquire()

        return noop(conn)


@asynccontextmanager
async def noop(
        conn: SAConnection,
) -> AsyncIterator[SAConnection]:
    yield conn
