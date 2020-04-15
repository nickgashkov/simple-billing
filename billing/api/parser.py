import json
from typing import Any, Dict, List, Mapping, NoReturn, Optional, Union

import marshmallow
from aiohttp import web
from webargs.aiohttpparser import AIOHTTPParser


class ErrorCode:
    INVALID_JSON = "INVALID_JSON"
    INVALID_VALUE = "INVALID_VALUE"


ALL = "__all__"


class CompliantAIOHTTPParser(AIOHTTPParser):
    """Consistently raises `400` error in correct format."""

    def handle_error(
            self,
            error: marshmallow.ValidationError,
            req: web.Request,
            schema: marshmallow.Schema,
            *,
            error_status_code: Optional[int],
            error_headers: Optional[Mapping[str, str]],
    ) -> NoReturn:
        raise web.HTTPBadRequest(
            body=_get_error_body_from_marshmallow(error),
            headers=error_headers,
            content_type="application/json",
        )

    def _handle_invalid_json_error(
            self,
            error: Union[json.JSONDecodeError, UnicodeDecodeError],
            req: web.Request,
            *args: Any,
            **kwargs: Any,
    ) -> NoReturn:
        raise web.HTTPBadRequest(
            body=_get_error_body(
                [
                    {
                        "code": ErrorCode.INVALID_JSON,
                        "message": "Invalid JSON body.",
                        "target": ALL,
                    },
                ],
            ),
            content_type="application/json",
        )


def _get_error_body_from_marshmallow(
        error: marshmallow.ValidationError,
) -> bytes:
    errors = []

    if isinstance(error.messages, dict):
        messages = error.messages["json"]
    else:
        messages = error.messages
    messages = {ALL: messages} if isinstance(messages, list) else messages

    for target, target_messages in messages.items():
        for target_message in target_messages:
            errors.append(
                {
                    "code": ErrorCode.INVALID_VALUE,
                    "message": target_message,
                    "target": target,
                }
            )

    return _get_error_body(errors)


def _get_error_body(errors: List[Dict[str, str]]) -> bytes:
    data = {
        "status": {
            "success": False,
            "errors": errors,
        },
        "data": None,
    }

    return json.dumps(data).encode()


parser = CompliantAIOHTTPParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
