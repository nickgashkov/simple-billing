from typing import Any, Awaitable, Callable

from aiohttp.test_utils import TestClient
from mypy_extensions import KwArg
from tests.fixtures.factories import UserModel, WalletFactory


async def test_user_can_retrieve_their_wallet(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        wallet_factory: WalletFactory,
) -> None:
    user = await login()
    wallet_factory.create(
        id='3fa85f64-5717-4562-b3fc-2c963f66afa6',
        user=user,
    )

    response = await cli.get('/v1/wallets')
    response_json = await response.json()

    actual = response_json['data']['id']
    expected = '3fa85f64-5717-4562-b3fc-2c963f66afa6'

    assert actual == expected


async def test_user_obtains_not_found_if_theres_no_wallet(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
) -> None:
    await login()

    response = await cli.get('/v1/wallets')
    response_json = await response.json()

    actual = (response.status, response_json['status']['errors'])
    expected = (
        404,
        [
            {
                'code': 'NOT_FOUND',
                'message': "Wallet does not exist.",
                'target': '__all__',
            }
        ]
    )

    assert actual == expected


async def test_retrieve_wallet_requires_login(cli: TestClient) -> None:
    response = await cli.get('/v1/wallets')
    response_json = await response.json()

    actual = (response.status, response_json['status']['errors'])
    expected = (
        401,
        [
            {
                'code': 'UNAUTHORIZED',
                'message': "Authentication required.",
                'target': '__all__',
            }
        ]
    )

    assert actual == expected
