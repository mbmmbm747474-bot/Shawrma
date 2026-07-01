from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings


ALGORITHM = "HS256"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    typ: str


def _create_token(
    subject: str,
    expires_delta: timedelta,
    token_type: str,
) -> str:

    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": subject,
        "exp": expire,
        "typ": token_type,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_access_token(
    subject: str | UUID,
    expires_delta: Optional[timedelta] = None,
) -> str:

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    return _create_token(
        subject=str(subject),
        expires_delta=expires_delta,
        token_type="access",
    )


def create_refresh_token(
    subject: str | UUID,
    expires_days: int = 30,
) -> str:

    return _create_token(
        subject=str(subject),
        expires_delta=timedelta(days=expires_days),
        token_type="refresh",
    )


def decode_token(token: str) -> TokenPayload:

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return TokenPayload(**payload)

    except JWTError as exc:
        raise ValueError("Invalid token") from exc


def decode_access_token(token: str) -> TokenPayload:

    payload = decode_token(token)

    if payload.typ != "access":
        raise ValueError("Invalid access token")

    return payload


def decode_refresh_token(token: str) -> TokenPayload:

    payload = decode_token(token)

    if payload.typ != "refresh":
        raise ValueError("Invalid refresh token")

    return payload
