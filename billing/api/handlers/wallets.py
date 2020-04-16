import decimal
import uuid

from aiohttp import web
from aiohttp_security import authorized_userid
from webargs import fields

from billing.api import responses
from billing.api.authentication import login_required
from billing.api.parser import use_kwargs
from billing.db.storage import (
    create_operation_deposit,
    create_operation_transfer,
    get_operations,
    get_wallet,
    get_wallet_balance,
)


@login_required
async def retrieve(request: web.Request) -> web.Response:
    user_id = await authorized_userid(request)
    wallet = await get_wallet(request.app['db'], user_id)

    if wallet is None:
        return responses.not_found("Wallet does not exist.")

    wallet_balance = await get_wallet_balance(request.app['db'], wallet.id)
    return responses.success(wallet.to_json(balance=wallet_balance))


@login_required
async def operations(request: web.Request) -> web.Response:
    user_id = await authorized_userid(request)
    wallet = await get_wallet(request.app['db'], user_id)

    if wallet is None:
        return responses.not_found("Wallet does not exist.")

    ops = await get_operations(request.app['db'], wallet.id)
    ops_json = [op.to_json() for op in ops]

    return responses.success(ops_json)


@login_required
@use_kwargs({"amount": fields.Decimal(places=2, required=True)})
async def deposit(
        request: web.Request,
        amount: decimal.Decimal,
) -> web.Response:
    user_id = await authorized_userid(request)
    wallet = await get_wallet(request.app['db'], user_id)

    if wallet is None:
        return responses.not_found("Wallet does not exist.")

    op = await create_operation_deposit(request.app['db'], wallet.id, amount)

    return responses.success(op.to_json())


@login_required
@use_kwargs(
    {
        "destination": fields.UUID(required=True),
        "amount": fields.Decimal(required=True),
    }
)
async def transfer(
        request: web.Request,
        destination: uuid.UUID,
        amount: decimal.Decimal,
) -> web.Response:
    user_id = await authorized_userid(request)
    wallet = await get_wallet(request.app['db'], user_id)

    if wallet is None:
        return responses.not_found("Wallet does not exist.")

    wallet_balance = await get_wallet_balance(request.app['db'], wallet.id)

    if wallet_balance < amount:
        return responses.bad_request("Insufficient funds.")

    ops = await create_operation_transfer(
        request.app['db'],
        source_wallet_id=wallet.id,
        destination_wallet_id=str(destination),
        amount=amount,
    )

    op = ops[0]

    return responses.success(op.to_json())
