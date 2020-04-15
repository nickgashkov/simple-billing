import json
from typing import Any, Dict, List, Mapping, NoReturn, Optional, Union

import marshmallow
from aiohttp import web
from webargs.aiohttpparser import AIOHTTPParser

from billing.api import responses
from billing.api.responses import TARGET_ALL, ErrorCode


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
        raise web.HTTPUnprocessableEntity(
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
        raise web.HTTPUnprocessableEntity(
            content_type="application/json",
            body=_get_error_body(
                [
                    {
                        "code": ErrorCode.BAD_REQUEST,
                        "message": "Invalid JSON body.",
                        "target": TARGET_ALL,
                    },
                ],
            ),
        )


def _get_error_body_from_marshmallow(
        error: marshmallow.ValidationError,
) -> bytes:
    errors = []

    if isinstance(error.messages, dict):
        messages = error.messages["json"]
    else:
        messages = error.messages

    if isinstance(messages, list):
        messages = {TARGET_ALL: messages}

    for target, target_messages in messages.items():
        for target_message in target_messages:
            errors.append(
                {
                    "code": ErrorCode.UNPROCESSABLE_ENTITY,
                    "message": target_message,
                    "target": target,
                }
            )

    return _get_error_body(errors)


def _get_error_body(errors: List[Dict[str, str]]) -> bytes:
    return json.dumps(responses.failure_body(errors)).encode()


parser = CompliantAIOHTTPParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
