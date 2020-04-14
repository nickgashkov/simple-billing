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
@click.option("--log-level", default="INFO")
@click.option("--port", type=int, default=8080)
def main(log_level: str, port: int) -> None:
    configure_logs(level=log_level)
    web.run_app(init_app(), port=port)


if __name__ == '__main__':
    main()
