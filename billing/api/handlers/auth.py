from aiohttp import web
from aiohttp_security import forget, remember
from webargs import fields

from billing.api import responses
from billing.api.parser import use_kwargs
from billing.api.validators.auth import validate_password_matches
from billing.auth.authentication import is_password_correct
from billing.db.storage import create_user, create_wallet, get_user


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
        return responses.unauthorized(message="Invalid username or password.")

    response = responses.success(user.to_json())
    await remember(request, response, username)
    return response


async def logout(request: web.Request) -> web.Response:
    response = responses.success(data=None)
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
        return responses.bad_request(
            message="This username already taken.",
            target="username",
        )

    user = await create_user(request.app['db'], username, password)
    await create_wallet(request.app['db'], user.id)

    response = responses.success(user.to_json())
    await remember(request, response, username)
    return response
