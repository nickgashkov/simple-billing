from aiohttp import web
from jibrel_aiohttp_swagger import setup_swagger

from billing import settings
from billing.api.handlers import monitoring
from billing.db.wrapper import Database


def init_app(db_dsn: str) -> web.Application:
    app = web.Application()
    app['db'] = Database(db_dsn)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    app.router.add_get('/healthcheck', monitoring.healthcheck)

    setup_swagger(
        app,
        spec_path=settings.SPEC_FILEPATH,
        version_file_path=settings.VERSION_FILEPATH,
    )

    return app


async def on_startup(app: web.Application) -> None:
    await app['db'].start()


async def on_shutdown(app: web.Application) -> None:
    await app['db'].stop()
