from typing import Any, Awaitable, Callable

from aiohttp.test_utils import TestClient
from mypy_extensions import KwArg
from tests.fixtures.factories import UserModel


async def test_user_can_logout(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
) -> None:
    await login()
    await cli.post('/v1/auth/logout')

    response = await cli.get('/__test__/identity')
    response_json = await response.json()

    assert response_json["authorized_userid"] is None


async def test_anonymous_user_can_logout(cli: TestClient) -> None:
    await cli.post('/v1/auth/logout')

    response = await cli.get('/__test__/identity')
    response_json = await response.json()

    assert response_json["authorized_userid"] is None
