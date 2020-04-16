import base64

import aiohttp_security
import aiohttp_session
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from jibrel_aiohttp_swagger import setup_swagger

from billing import settings
from billing.api.handlers import auth, monitoring, wallets
from billing.auth.authorization import DbAuthorizationPolicy
from billing.db.wrapper import Database


def init_app(
        db_dsn: str,
        secret_key: str,
        session_cookie_name: str,
) -> web.Application:
    app = web.Application()
    app['db'] = Database(db_dsn)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    app.router.add_post('/v1/auth/login', auth.login)
    app.router.add_post('/v1/auth/logout', auth.logout)
    app.router.add_post('/v1/auth/register', auth.register)

    app.router.add_get('/v1/wallets', wallets.retrieve)
    app.router.add_get('/v1/wallets/operations', wallets.operations)
    app.router.add_post('/v1/wallets/deposit', wallets.deposit)
    app.router.add_post('/v1/wallets/transfer', wallets.transfer)

    app.router.add_get('/healthcheck', monitoring.healthcheck)

    setup_session(app, secret_key, session_cookie_name)
    setup_security(app)
    setup_swagger(
        app,
        spec_path=settings.SPEC_FILEPATH,
        version_file_path=settings.VERSION_FILEPATH,
    )

    return app


def setup_session(
        app: web.Application,
        secret_key: str,
        session_cookie_name: str,
) -> None:
    aiohttp_session.setup(
        app, EncryptedCookieStorage(
            base64.urlsafe_b64decode(secret_key),
            cookie_name=session_cookie_name,
        ),
    )


def setup_security(app: web.Application) -> None:
    aiohttp_security.setup(
        app, SessionIdentityPolicy(), DbAuthorizationPolicy(app['db']),
    )


async def on_startup(app: web.Application) -> None:
    await app['db'].start()


async def on_shutdown(app: web.Application) -> None:
    await app['db'].stop()
