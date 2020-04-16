#!/bin/bash -e

echo "Starting Simple Billing service, mode '$1' version '`cat /app/billing/version.txt`' on node '`hostname`'"
dockerize -wait tcp://`python -c 'import dsnparse; p = dsnparse.parse_environ("BILLING_DB_DSN", hostname="localhost", port="5432"); print(p.hostloc)'`
exec "$@"
