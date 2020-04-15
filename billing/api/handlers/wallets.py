import decimal
from typing import Optional

from aiohttp import web
from aiohttp_security import authorized_userid
from webargs import fields

from billing.api import responses
from billing.api.authentication import login_required
from billing.api.parser import use_kwargs
from billing.db.storage import (
    create_operation_faucet,
    create_wallet,
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
    return web.json_response()


@login_required
@use_kwargs({"faucet": fields.Decimal(places=2, required=False)})
async def create(
        request: web.Request,
        faucet: Optional[decimal.Decimal] = None,
) -> web.Response:
    user_id = await authorized_userid(request)
    already_created_wallet = await get_wallet(request.app['db'], user_id)

    if already_created_wallet is not None:
        return responses.bad_request(message="Wallet already exists.")

    wallet = await create_wallet(request.app['db'], user_id)

    if faucet:
        await create_operation_faucet(
            request.app['db'],
            wallet.id,
            amount=faucet,
        )

    wallet_balance = await get_wallet_balance(request.app['db'], wallet.id)

    return responses.created(wallet.to_json(balance=wallet_balance))


@login_required
async def transfer(request: web.Request) -> web.Response:
    return web.json_response()
