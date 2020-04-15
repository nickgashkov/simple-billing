from typing import Dict

import pytest
from aiohttp.test_utils import TestClient
from tests.fixtures.factories import UserFactory


async def test_user_can_successfully_login_with_valid_credentials(
        cli: TestClient,
        user_factory: UserFactory,
) -> None:
    user_factory.create(
        id='3fa85f64-5717-4562-b3fc-2c963f66afa6',
        username='admin',
        password_raw='pass',
    )

    await cli.post('/v1/auth/login', json={
        'username': 'admin',
        'password': 'pass',
    })

    response = await cli.get('/__test__/identity')
    response_json = await response.json()

    actual = response_json["authorized_userid"]
    expected = '3fa85f64-5717-4562-b3fc-2c963f66afa6'

    assert actual == expected


async def test_user_cannot_login_with_invalid_credentials(
        cli: TestClient,
        user_factory: UserFactory,
) -> None:
    user_factory.create(username='admin', password_raw='pass')

    response = await cli.post('/v1/auth/login', json={
        'username': 'admin',
        'password': 'pwd',
    })
    response_json = await response.json()

    actual = (response.status, response_json['status']['errors'])
    expected = (
        401,
        [
            {
                'code': 'UNAUTHORIZED',
                'message': "Invalid username or password.",
                'target': '__all__',
            },
        ],
    )

    assert actual == expected


@pytest.mark.parametrize(
    'body, error',
    (
        (
            {'password': 'pass'},
            {
                'code': 'UNPROCESSABLE_ENTITY',
                'message': "Missing data for required field.",
                'target': 'username',
            },
        ),
        (
            {'username': 'admin'},
            {
                'code': 'UNPROCESSABLE_ENTITY',
                'message': "Missing data for required field.",
                'target': 'password',
            },
        ),
    ),
    ids=[
        'username missing',
        'password missing',
    ]
)
async def test_login_user_sad_paths(
        cli: TestClient,
        body: Dict[str, str],
        error: Dict[str, str],
) -> None:
    response = await cli.post('/v1/auth/login', json=body)
    response_json = await response.json()

    actual = (response.status, response_json["status"]["errors"])
    expected = (422, [error])
    assert actual == expected
