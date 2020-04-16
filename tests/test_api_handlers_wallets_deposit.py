from typing import Any, Awaitable, Callable, Optional

import pytest
from aiohttp.test_utils import TestClient
from mypy_extensions import KwArg
from tests.fixtures.factories import UserModel, WalletFactory


@pytest.mark.parametrize('amount', ('1000.42', '0.01'))
async def test_user_can_perform_deposit(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        amount: Optional[str],
        wallet_factory: WalletFactory,
) -> None:
    user = await login()
    wallet_factory.create(user=user)

    response = await cli.post('/v1/wallets/deposit', json={'amount': amount})
    response_json = await response.json()

    actual = (response.status, response_json['data']['amount'])
    expected = (200, amount)

    assert actual == expected


async def test_user_cannot_deposit_wallet_with_invalid_amount(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
) -> None:
    await login()

    response = await cli.post('/v1/wallets/deposit', json={'amount': 'string'})
    response_json = await response.json()

    actual = (response.status, response_json['status']['errors'])
    expected = (
        422,
        [
            {
                'code': 'UNPROCESSABLE_ENTITY',
                'message': 'Not a valid number.',
                'target': 'amount',
            }
        ],
    )

    assert actual == expected


async def test_deposit_requires_existing_wallet(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
) -> None:
    await login()

    response = await cli.post('/v1/wallets/deposit', json={'amount': '10.00'})
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


async def test_create_wallet_requires_login(cli: TestClient) -> None:
    response = await cli.post('/v1/wallets/deposit')
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
