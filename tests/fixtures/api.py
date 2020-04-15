from asyncio import AbstractEventLoop
from typing import Any, Awaitable, Callable, Optional

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp_security import authorized_userid
from mypy_extensions import KwArg
from tests.fixtures.factories import UserFactory, UserModel

from billing import settings
from billing.api.app import init_app


@pytest.fixture
def cli(
        loop: AbstractEventLoop,
        aiohttp_client: Callable[[web.Application], Awaitable[TestClient]],
) -> TestClient:
    app = init_app(
        db_dsn=settings.DB_DSN_TEST,
        secret_key="NQLSo4kyVKvWRDeo4tP_z25GPK4pN4vvrb14zv4SXI8=",
        session_cookie_name="sessionid",
    )
    client = aiohttp_client(app)

    app.router.add_get('/__test__/identity', _get_user_identity)

    return loop.run_until_complete(client)


async def _get_user_identity(request: web.Request) -> web.Response:
    return web.json_response(
        {
            "authorized_userid": await authorized_userid(request)
        }
    )


@pytest.fixture()
async def login(
        cli: TestClient,
        user_factory: UserFactory,
) -> Callable[[KwArg(Any)], Awaitable[UserModel]]:
    async def login_(
            user: Optional[UserModel] = None,
            **kwargs: Any,
    ) -> UserModel:
        kwargs.setdefault('password_raw', 'pass')
        user = user or user_factory.create(**kwargs)

        await cli.post('/v1/auth/login', json={
            'username': user.username,
            'password': kwargs['password_raw'],
        })

        return user

    return login_
