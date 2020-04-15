import decimal
from typing import Any, Awaitable, Callable, Dict

import pytest
from aiohttp.test_utils import TestClient
from mypy_extensions import KwArg
from tests.fixtures.factories import (
    OperationFactory,
    UserFactory,
    UserModel,
    WalletFactory,
)


async def test_user_can_transfer_money_to_another_user(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        user_factory: UserFactory,
        wallet_factory: WalletFactory,
        operation_factory: OperationFactory,
) -> None:
    source_user = user_factory.create(password_raw='pass')
    destination_user = user_factory.create(password_raw='pass')

    source_wallet = wallet_factory.create(user=source_user)
    destination_wallet = wallet_factory.create(user=destination_user)

    operation_factory.create(
        wallet=source_wallet,
        destination_wallet=source_wallet,
        amount=decimal.Decimal('1000'),
    )

    await login(user=source_user)
    await cli.post('/v1/wallets/transfer', json={
        'destination': destination_wallet.id,
        'amount': '50.00',
    })

    source_response = await cli.get('/v1/wallets')
    source_response_json = await source_response.json()

    await login(user=destination_user)

    destination_response = await cli.get('/v1/wallets')
    destination_response_json = await destination_response.json()

    actual = (
        source_response_json['data']['balance'],
        destination_response_json['data']['balance'],
    )
    expected = ('950.00', '50.00')

    assert actual == expected


async def test_user_without_wallet_gets_not_found_error(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
) -> None:
    await login()

    response = await cli.post('/v1/wallets/transfer', json={
        'destination': '1bb41739-afb5-41c5-aaee-b344f7066bf9',
        'amount': '50.00',
    })
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


async def test_user_cannot_transfer_if_them_has_insufficient_funds(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        wallet_factory: WalletFactory,
) -> None:
    user = await login()
    wallet_factory.create(user=user)

    response = await cli.post('/v1/wallets/transfer', json={
        'destination': '1bb41739-afb5-41c5-aaee-b344f7066bf9',
        'amount': '50.00',
    })
    response_json = await response.json()

    actual = (response.status, response_json['status']['errors'])
    expected = (
        400,
        [
            {
                'code': 'BAD_REQUEST',
                'message': "Insufficient funds.",
                'target': '__all__',
            }
        ]
    )

    assert actual == expected


async def test_transfer_requires_login(cli: TestClient) -> None:
    response = await cli.post('/v1/wallets/transfer')
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


@pytest.mark.parametrize(
    'body, error',
    (
        (
            {
                'amount': '42.12'
            },
            {
                'code': 'UNPROCESSABLE_ENTITY',
                'message': "Missing data for required field.",
                'target': 'destination',
            },
        ),
        (
            {
                'destination': '1bb41739-afb5-41c5-aaee-b344f7066bf9',
            },
            {
                'code': 'UNPROCESSABLE_ENTITY',
                'message': "Missing data for required field.",
                'target': 'amount',
            },
        ),
        (
            {
                'amount': 'string',
                'destination': '1bb41739-afb5-41c5-aaee-b344f7066bf9',
            },
            {
                'code': 'UNPROCESSABLE_ENTITY',
                'message': "Not a valid number.",
                'target': 'amount',
            },
        ),
        (
            {
                'amount': '42.12',
                'destination': 'string',
            },
            {
                'code': 'UNPROCESSABLE_ENTITY',
                'message': "Not a valid UUID.",
                'target': 'destination',
            },
        ),
    ),
    ids=[
        'missing destination',
        'missing amount',
        'invalid amount',
        'invalid destination',
    ]
)
async def test_register_user_validation_errors(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        body: Dict[str, str],
        error: Dict[str, str],
) -> None:
    await login()

    response = await cli.post('/v1/wallets/transfer', json=body)
    response_json = await response.json()

    assert response.status == 422
    assert response_json["status"]["errors"] == [error]
