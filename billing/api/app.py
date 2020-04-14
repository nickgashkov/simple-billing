from aiohttp import web
from jibrel_aiohttp_swagger import setup_swagger

from billing import settings
from billing.api.handlers import monitoring


def init_app() -> web.Application:
    app = web.Application()
    app.router.add_get('/healthcheck', monitoring.healthcheck)

    setup_swagger(
        app,
        spec_path=settings.SPEC_FILEPATH,
        version_file_path=settings.VERSION_FILEPATH,
    )

    return app
