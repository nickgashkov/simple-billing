import functools
from typing import Any, Dict, List

from aiohttp import web

TARGET_ALL = "__all__"


class ErrorCode:
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    NOT_FOUND = "NOT_FOUND"
    UNPROCESSABLE_ENTITY = "UNPROCESSABLE_ENTITY"


def bad_request(message: str, target: str = TARGET_ALL) -> web.Response:
    return web.json_response(
        status=400,
        data=failure_body(
            [
                {
                    'code': ErrorCode.BAD_REQUEST,
                    'message': message,
                    'target': target,
                }
            ]
        )
    )


def unauthorized(message: str = 'Authentication required.') -> web.Response:
    return web.json_response(
        status=401,
        data=failure_body(
            [
                {
                    'code': ErrorCode.UNAUTHORIZED,
                    'message': message,
                    'target': TARGET_ALL,
                }
            ]
        )
    )


def not_found(message: str) -> web.Response:
    return web.json_response(
        status=404,
        data=failure_body(
            [
                {
                    'code': ErrorCode.NOT_FOUND,
                    'message': message,
                    'target': TARGET_ALL,
                }
            ]
        )
    )


def unprocessable(message: str, target: str = TARGET_ALL) -> web.Response:
    return web.json_response(
        status=422,
        data=failure_body(
            [
                {
                    'code': ErrorCode.UNPROCESSABLE_ENTITY,
                    'message': message,
                    'target': target,
                }
            ]
        )
    )


def success(data: Any, status: int = 200) -> web.Response:
    return web.json_response(data=success_body(data), status=status)


created = functools.partial(success, status=201)


def success_body(data: Any) -> Dict[str, Any]:
    return {
        "status": {
            "success": True,
            "errors": [],
        },
        "data": data,
    }


def failure_body(errors: List[Dict[str, str]]) -> Dict[str, Any]:
    return {
        "status": {
            "success": False,
            "errors": errors,
        },
        "data": None,
    }
