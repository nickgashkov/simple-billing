from aiohttp import web

from billing.api.handlers import monitoring


def init_app() -> web.Application:
    app = web.Application()
    app.router.add_get('/healthcheck', monitoring.healthcheck)

    return app
