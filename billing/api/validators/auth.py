from typing import Any, Dict

from marshmallow import ValidationError


def validate_password_matches(args: Dict[str, Any]) -> None:
    if args["password"] == args["password_confirm"]:
        return

    raise ValidationError(message="Password does not match it's confirmation.")
