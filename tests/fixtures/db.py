import subprocess
from typing import Generator

import pytest


@pytest.fixture(scope="session", autouse=True)
def migrate_db() -> Generator[None, None, None]:
    migrate_db_up()
    yield
    migrate_db_down()


def migrate_db_up() -> None:
    subprocess.run(
        [
            'dbmate',
            '-d', '"./billing/migrations"',
            '-e', 'BILLING_DB_DSN_TEST',
            'up',
        ],
    )


def migrate_db_down() -> None:
    done = False

    while not done:
        done = migrate_db_down_once()


def migrate_db_down_once() -> bool:
    proc = subprocess.run(
        [
            'dbmate',
            '-d', '"./billing/migrations"',
            '-e', 'BILLING_DB_DSN_TEST',
            'down',
        ],
        capture_output=True,
    )

    output = proc.stderr.decode()
    done = "Error: can't rollback: no migrations have been applied" in output

    return done