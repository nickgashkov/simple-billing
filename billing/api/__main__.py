import click
from aiohttp import web

from billing.api.app import init_app


@click.command(
    context_settings={
        "auto_envvar_prefix": "BILLING",
        "show_default": True,
    },
)
@click.option("--port", type=int, default=8080)
def main(port: int) -> None:
    web.run_app(init_app(), port=port)


if __name__ == '__main__':
    main()
