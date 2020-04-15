from typing import Dict

import pytest
from aiohttp.test_utils import TestClient


async def test_register_user_happy_path(cli: TestClient) -> None:
    response = await cli.post('/v1/auth/register', json={
        'username': 'admin',
        'password': 'pass',
        'passwordConfirm': 'pass',
    })
    response_json = await response.json()

    assert response.status == 200
    assert response_json["data"]["username"] == "admin"


@pytest.mark.parametrize(
    'body, error',
    (
        (
            {
                'username': 'admin',
                'password': 'pass',
                'passwordConfirm': '123',
            },
            {
                'code': 'INVALID_VALUE',
                'message': "Password does not match it's confirmation.",
                'target': '__all__',
            },
        ),
        (
            {
                'password': 'pass',
                'passwordConfirm': '123',
            },
            {
                'code': 'INVALID_VALUE',
                'message': "Missing data for required field.",
                'target': 'username',
            },
        ),
        (
            {
                'username': 'admin',
                'passwordConfirm': '123',
            },
            {
                'code': 'INVALID_VALUE',
                'message': "Missing data for required field.",
                'target': 'password',
            },
        ),
        (
            {
                'username': 'admin',
                'password': 'pass',
            },
            {
                'code': 'INVALID_VALUE',
                'message': "Missing data for required field.",
                'target': 'passwordConfirm',
            },
        ),
    ),
    ids=[
        'password does not match with confirmation',
        'username missing',
        'password missing',
        'passwordConfirm missing',
    ]
)
async def test_register_user_validation_errors(
        cli: TestClient,
        body: Dict[str, str],
        error: Dict[str, str],
) -> None:
    response = await cli.post('/v1/auth/register', json=body)
    response_json = await response.json()

    assert response.status == 400
    assert response_json["status"]["errors"] == [error]
