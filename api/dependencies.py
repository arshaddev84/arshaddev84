import os
from typing import Any
from uuid import uuid4

import jwt
from fastapi import Request

from .exceptions import UnauthorizedError


def get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id", str(uuid4()))


def get_request_context(request: Request) -> dict[str, Any]:
    return {"request_id": get_request_id(request)}


def require_authenticated_user(request: Request) -> dict[str, Any]:
    auth_header = request.headers.get("authorization", "")

    if not auth_header.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid bearer token")
    
    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        raise UnauthorizedError("Missing bearer token")

    secret_key = os.getenv(JWT_SECRET_KEY)
    if not secret_key:
        raise UnauthorizedError("Authentication configuration missing")

    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    decode_kwargs: dict[str, Any] = {
        "algorithms": [algorithm],
        "options": {"require": ["exp", "sub"]},
        "leeway": 5,
    }

    issuer = os.getenv("JWT_ISSUER")
    audience = os.getenv("JWT_AUDIENCE")
    if issuer:
        decode_kwargs["issuer"] = issuer
    if audience:
        decode_kwargs["audience"] = audience

    try:
        payload = jwt.decode(token, secret_key, **decode_kwargs)
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedError("Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedError("Invalid token") from exc

    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject.strip():
        raise UnauthorizedError("Invalid token claims")
    
    return {
        "sub": subject,
        "request_id": get_request_id(request),
        "claims": payload
    }