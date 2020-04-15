from aiohttp import web
from aiohttp_security import forget, remember
from webargs import fields

from billing.api.bodies import json_failure, json_success
from billing.api.parser import use_kwargs
from billing.api.validators.auth import validate_password_matches
from billing.auth.authentication import is_password_correct
from billing.db.storage import create_user, get_user


@use_kwargs(
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)
async def login(
        request: web.Request,
        username: str,
        password: str,
) -> web.Response:
    user = await get_user(request.app['db'], username)
    success = user and is_password_correct(password, user.password)

    if not success or not user:
        return web.json_response(
            status=401,
            data=json_failure(
                errors=[
                    {
                        'code': 'INVALID_VALUE',
                        'message': 'Invalid username or password.',
                        'target': '__all__',
                    }
                ],
            )
        )

    response = web.json_response(json_success(data=user.to_json()))
    await remember(request, response, username)
    return response


async def logout(request: web.Request) -> web.Response:
    response = web.json_response(json_success(data=None))
    await forget(request, response)
    return response


@use_kwargs(
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
        "password_confirm": fields.String(
            required=True,
            data_key="passwordConfirm",
        ),
    },
    validate=validate_password_matches,
)
async def register(
        request: web.Request,
        username: str,
        password: str,
        password_confirm: str,
) -> web.Response:
    user_with_requested_username = await get_user(request.app['db'], username)

    if user_with_requested_username is not None:
        return web.json_response(
            status=400,
            data=json_failure(
                [
                    {
                        'code': 'INVALID_VALUE',
                        'message': 'This username already taken.',
                        'target': 'username',
                    }
                ]
            ),
        )

    await create_user(request.app['db'], username, password)
    user = await get_user(request.app['db'], username)

    if not user:
        raise web.HTTPInternalServerError()

    response = web.json_response(json_success(data=user.to_json()))
    await remember(request, response, username)
    return response
