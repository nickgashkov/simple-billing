from typing import Any, Dict, List, Optional

import aiopg.sa
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

    async def execute(self, query: ClauseElement) -> None:
        async with self.engine.acquire() as conn:
            await conn.execute(query)

    async def all(self, query: ClauseElement) -> Rows:
        async with self.engine.acquire() as conn:
            cursor = await conn.execute(query)
            results = await cursor.fetchall()
        return [dict(item) for item in results]

    async def one(self, query: ClauseElement) -> Optional[Row]:
        async with self.engine.acquire() as conn:
            cursor = await conn.execute(query)
            result = await cursor.fetchone()

        return dict(result) if result else None
