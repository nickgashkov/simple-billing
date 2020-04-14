from asyncio import AbstractEventLoop
from typing import Awaitable, Callable

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from billing import settings
from billing.api.app import init_app


@pytest.fixture
def cli(
        loop: AbstractEventLoop,
        aiohttp_client: Callable[[web.Application], Awaitable[TestClient]],
) -> TestClient:
    app = init_app(db_dsn=settings.DB_DSN_TEST)
    client = aiohttp_client(app)

    return loop.run_until_complete(client)
