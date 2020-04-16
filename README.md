# Simple Billing API ![Build Status](https://github.com/nickgashkov/simple-billing/workflows/build/badge.svg)

**Simple Billing API** is a sample application showcasing Python and PostgreSQL
as backend technologies to build financial applications.

## Prerequisites

To run **Simple Billing API**, [Docker](https://docs.docker.com/install/) must be
installed.

## Building

**Simple Billing API** can be built using `make`:

```
$ make build
```

## Running

**Simple Billing API** can be run using `make` as well:

```
$ make run
```

Before running, this command will build Docker container and run pending
migrations if any exists. 

API can be accessed at http://localhost:8080.

### Examples

API can be interacted with via cURL, HTTPie, Postman or via Swagger at
http://localhost:8080/api/doc/. Also, quick API showcase can be found on
YouTube:

[![Simple Billing API Showcase](https://img.youtube.com/vi/jigONBp4G8M/0.jpg)](https://youtu.be/jigONBp4G8M)

## Design trade-offs

Everything related to request-response cycle is pretty much standard and
there're no hack-y decisions there:
- Validation of incoming requests is done via `webargs` library powered
internally by `marshmallow`
- Authentication is built upon `aiohttp-security` — first-party authz
extension.
- All response's data objects are pretty simple, so just regular `NamedTuple`
serialization is used.

Some storage hacks have slept into the code though.

### No denormalized "wallets"."balance"
There no pre-calculated balance of users' wallets. This design decision allows
reverting operations, optionally adding their state in the future.

The trade-off is obviously the performance. Upon each `/v1/wallets` request,
all wallet's operations' amounts are pulled from the database with calculation
in Python. This approch works fairly good for wallets with ~10000 operations
but will eventually become a bottleneck for more active users.

Calculation in-Python allows API to take significant amount of aggregation work
from the database and allows for easier horizontal scaling without database
sharding.

### Two "operations" per each transfer
Upon each transfer, two `operations` are created for each wallet for both
source and destination wallets. Operations differ by the amount sign (negative
for the sender and positive for the destination) and
`"operations"."wallet_id"`.

This approach allows fetching all user-related transaction with a simple query
without `OR` clauses like:

```postgresql
SELECT * FROM operations WHERE wallet_id = '<uuid>';
```

This hack is targeted towards performance improvements with an additional
occupied space trade-off.

`"operations"` will likely be the biggest table in the database. Therefore,
this approach ensures that database with easily retrieve those datasets.
