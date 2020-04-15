import functools
from typing import Any, Awaitable, Callable

from aiohttp import web
from aiohttp_security import authorized_userid

from billing.api import responses

AiohttpHandler = Callable[[web.Request], Awaitable[web.Response]]


def login_required(func: AiohttpHandler) -> AiohttpHandler:
    @functools.wraps(func)
    async def wrapper(
            request: web.Request,
            *args: Any,
            **kwargs: Any,
    ) -> web.Response:
        userid = await authorized_userid(request)

        if userid is None:
            return responses.unauthorized()

        return await func(request, *args, **kwargs)  # type: ignore

    return wrapper
