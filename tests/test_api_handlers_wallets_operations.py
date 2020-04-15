from typing import Any, Awaitable, Callable

from aiohttp.test_utils import TestClient
from mypy_extensions import KwArg
from tests.fixtures.factories import OperationFactory, UserModel, WalletFactory


async def test_user_can_retrieve_their_operations(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        wallet_factory: WalletFactory,
        operation_factory: OperationFactory,
) -> None:
    user = await login()
    wallet = wallet_factory.create(user=user)

    for id in [
        '3fa85f64-5717-4562-b3fc-2c963f66afa6',
        '1bb41739-afb5-41c5-aaee-b344f7066bf9',
        'c49ef2aa-ca2d-4c71-aaab-4e1cca2c899a',
    ]:
        operation_factory.create(
            id=id,
            wallet=wallet,
            destination_wallet=wallet,
        )

    response = await cli.get('/v1/wallets/operations')
    response_json = await response.json()

    actual = {entry['id'] for entry in response_json['data']}
    expected = {
        '3fa85f64-5717-4562-b3fc-2c963f66afa6',
        '1bb41739-afb5-41c5-aaee-b344f7066bf9',
        'c49ef2aa-ca2d-4c71-aaab-4e1cca2c899a',
    }

    assert actual == expected


async def test_user_without_wallet_gets_not_found_error(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
) -> None:
    await login()

    response = await cli.get('/v1/wallets/operations')
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


async def test_user_cannot_see_operations_of_another_user(
        cli: TestClient,
        login: Callable[[KwArg(Any)], Awaitable[UserModel]],
        wallet_factory: WalletFactory,
        operation_factory: OperationFactory,
) -> None:
    user = await login()
    wallet = wallet_factory.create(user=user)

    operation_factory.create(
        id='c49ef2aa-ca2d-4c71-aaab-4e1cca2c899a',
        wallet=wallet,
        destination_wallet=wallet,
    )

    response = await cli.get('/v1/wallets/operations')
    response_json = await response.json()

    actual = [entry['id'] for entry in response_json['data']]
    expected = ['c49ef2aa-ca2d-4c71-aaab-4e1cca2c899a']

    assert actual == expected


async def test_retrieve_wallet_requires_login(cli: TestClient) -> None:
    response = await cli.get('/v1/wallets/operations')
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
