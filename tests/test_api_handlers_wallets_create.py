from typing import Any, Awaitable, Callable, Optional

import pytest
from aiohttp.test_utils import TestClient
from mypy_extensions import KwArg
from tests.fixtures.factories import UserModel, WalletFactory


@pytest.mark.parametrize(
    'faucet, expected_balance',
    (
        ('1000.42', '1000.42'),
        ('0.00', '0.00'),
        (None, '0.00'),
    )
)
async def test_user_can_create_their_wallet(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        faucet: Optional[str],
        expected_balance: str,
) -> None:
    await login()

    request_json = {} if faucet is None else {'faucet': faucet}
    response = await cli.post('/v1/wallets', json=request_json)
    response_json = await response.json()

    actual = (response.status, response_json['data']['balance'])
    expected = (201, expected_balance)

    assert actual == expected


async def test_user_cannot_create_wallet_with_invalid_faucet(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
) -> None:
    await login()

    response = await cli.post('/v1/wallets', json={'faucet': 'string'})
    response_json = await response.json()

    actual = (response.status, response_json['status']['errors'])
    expected = (
        422,
        [
            {
                'code': 'UNPROCESSABLE_ENTITY',
                'message': 'Not a valid number.',
                'target': 'faucet',
            }
        ],
    )

    assert actual == expected


async def test_user_cannot_create_wallet_if_them_already_has_one(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        wallet_factory: WalletFactory,
) -> None:
    user = await login()
    wallet_factory.create(user=user)

    response = await cli.post('/v1/wallets')
    response_json = await response.json()

    actual = (response.status, response_json['status']['errors'])
    expected = (
        400,
        [
            {
                'code': 'BAD_REQUEST',
                'message': 'Wallet already exists.',
                'target': '__all__',
            }
        ],
    )

    assert actual == expected


async def test_retrieve_wallet_requires_login(cli: TestClient) -> None:
    response = await cli.post('/v1/wallets')
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
