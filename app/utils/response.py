"""
Standardized API Response Helper (Chapter 7 Concept).

Chapter 7 always wraps responses in a consistent format:
    { "message": "...", "data": { ... } }

This helper ensures every endpoint returns a uniform structure,
making it easier for frontend clients to consume the API.

Usage:
    from app.utils.response import success_response, error_response

    return success_response("token_generated", {"token": token})
    return error_response("invalid_credentials", status_code=401)
"""

from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(message: str, data: Any = None) -> dict:
    """
    Build a standardized success response matching Chapter 7's format.

    Example output:
        { "message": "token_generated", "data": { "token": "..." } }
    """
    response = {"message": message}
    if data is not None:
        response["data"] = data
    return response


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """
    Build a standardized error response matching Chapter 7's format.

    Example output:
        { "message": "invalid_credentials" }
    """
    return JSONResponse(
        status_code=status_code,
        content={"message": message},
    )
