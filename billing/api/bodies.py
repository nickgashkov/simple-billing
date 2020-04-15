from typing import Any, Dict, List


def json_success(data: Any) -> Dict[str, Any]:
    return {
        "status": {
            "success": True,
            "errors": [],
        },
        "data": data,
    }


def json_failure(errors: List[Dict[str, str]]) -> Dict[str, Any]:
    return {
        "status": {
            "success": False,
            "errors": errors,
        },
        "data": None,
    }
