from aiohttp import web


async def healthcheck(request: web.Request) -> web.Response:
    return web.json_response({'healthy': True})
