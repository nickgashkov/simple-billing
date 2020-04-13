from asyncio import AbstractEventLoop
from typing import Awaitable, Callable

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from billing.api.app import init_app


@pytest.fixture
def cli(
        loop: AbstractEventLoop,
        aiohttp_client: Callable[[web.Application], Awaitable[TestClient]],
) -> TestClient:
    return loop.run_until_complete(aiohttp_client(init_app()))
