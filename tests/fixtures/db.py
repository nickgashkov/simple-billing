import subprocess
from typing import AsyncGenerator, Generator

import pytest
from sqlalchemy import delete

from billing import settings
from billing.db.tables import tables
from billing.db.wrapper import Database


@pytest.fixture(scope="session", autouse=True)
def migrate_db() -> Generator[None, None, None]:
    migrate_db_up()
    yield
    migrate_db_down()


@pytest.fixture(autouse=True)
async def truncate_db(db: Database) -> AsyncGenerator[None, None]:
    yield
    for table in tables:
        await db.execute(delete(table))


@pytest.fixture()
def db_dsn() -> str:
    return settings.DB_DSN_TEST


@pytest.fixture()
async def db(db_dsn: str) -> AsyncGenerator[Database, None]:
    database = Database(dsn=settings.DB_DSN_TEST)

    await database.start()
    yield database

    await database.stop()


def migrate_db_up() -> None:
    subprocess.run(
        [
            'dbmate',
            '-d', str(settings.MIGRATIONS_DIRPATH.resolve()),
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
            '-d', str(settings.MIGRATIONS_DIRPATH.resolve()),
            '-e', 'BILLING_DB_DSN_TEST',
            'down',
        ],
        capture_output=True,
    )

    output = proc.stderr.decode()
    done = "Error: can't rollback: no migrations have been applied" in output

    return done
