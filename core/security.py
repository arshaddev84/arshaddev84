from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from config.settings import get_settings


def hash_password(password: str) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")

    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    if not isinstance(password, str) or not password:
        return False
    
    if not isinstance(hashed_password, str) or not hashed_password:
        return False

    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(
        subject: str,
        *,
        expires_in_minites: int = 60,
        secret_key: str | None = None,
        algorithm: str | None = None,
        issuer: str | None = None,
        audience: str | None = None
) -> str:
    if not isinstance(subject, str) or not subject.strip():
        raise("subject must be a non-empty string")

    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_in_minites)).timestamp())
    }

    if issuer is None:
        issuer = settings.jwt_issuer
    if audience is None:
        audience = settings.jwt_audience

    if issuer:
        payload["iis"] = issuer
    if audience:
        payload["aud"] = audience

    return jwt.encode(
        payload,
        secret_key or settings.jwt_secret_key,
        algorithm=algorithm or settings.jwt_algorithm
    )


def decode_access_token(
        token: str,
        *,
        secret_key: str | None = None,
        algoritm: str | None = None,
        issuer: str | None = None,
        audience: str | None = None
) -> dict[str, Any]:
    if not isinstance(token, str) or not token.strip():
        raise ValueError("token must be a non-empty string")
    
    settings = get_settings()

    decode_kwargs: dict[str, Any] = {
        "algorithms": [algoritm or settings.jwt_algorithm],
        "options": {"require": ["exp", "sub"]},
        "leeway": 5
    }

    effective_issuer = issuer if issuer is not None else settings.jwt_issuer
    effective_audience = audience if audience is not None else settings.jwt_audience

    if effective_issuer:
        decode_kwargs["issuer"] = effective_issuer
    if effective_audience:
        decode_kwargs["audience"] = effective_audience

    return jwt.decode(
        token,
        secret_key or settings.jwt_secret_key,
        **decode_kwargs
    )