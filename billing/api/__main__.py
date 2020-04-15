import click
from aiohttp import web

from billing.api.app import init_app
from billing.logs import configure_logs


@click.command(
    context_settings={
        "auto_envvar_prefix": "BILLING",
        "show_default": True,
    },
)
@click.option("--db-dsn")
@click.option("--secret-key")
@click.option("--session-cookie-name", default="sessionid")
@click.option("--log-level", default="INFO")
@click.option("--api-port", type=int, default=8080)
def main(
        db_dsn: str,
        secret_key: str,
        session_cookie_name: str,
        log_level: str,
        api_port: int,
) -> None:
    configure_logs(level=log_level)
    app = init_app(
        db_dsn=db_dsn,
        secret_key=secret_key,
        session_cookie_name=session_cookie_name,
    )
    web.run_app(app, port=api_port)


if __name__ == '__main__':
    main()
