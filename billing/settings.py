import os
from pathlib import Path

ROOT = Path(__file__).parent
SPEC_FILEPATH = ROOT / 'api' / 'v1.openapi.yml'
VERSION_FILEPATH = ROOT / 'version.txt'
MIGRATIONS_DIRPATH = ROOT / 'migrations'

DB_DSN_TEST = os.environ["BILLING_DB_DSN_TEST"]
