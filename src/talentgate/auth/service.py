import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from pytography import JsonWebToken, PasswordHashLibrary
from redis import Redis
from sqlmodel import Session, select

from src.talentgate.auth.models import BlacklistToken, TokenBlacklist


def encode_password(password: str) -> str:
    return PasswordHashLibrary.encode(password=password)


def verify_password(password: str, encoded_password: str) -> bool:
    return PasswordHashLibrary.verify(
        password=password,
        encoded_password=encoded_password,
    )


def encode_token(user_id: str, key: str, seconds: float) -> str:
    now = datetime.now(UTC)
    exp = (now + timedelta(seconds=seconds)).timestamp()
    jti = str(uuid.uuid4())
    payload = {
        "user_id": user_id,
        "exp": exp,
    }
    return JsonWebToken.encode(payload=payload, key=key)


def decode_token(token: str) -> tuple[dict, dict, str]:
    return JsonWebToken.decode(token=token)


def verify_token(token: str, key: str) -> bool:
    return JsonWebToken.verify(token=token, key=key)


def retrieve_blacklisted_token_v2(
    *, redis_client: Redis, jti: str | None
) -> str | None:
    name = f"token:blacklist:{jti}"
    return redis_client.get(name=name)


def revoke_token_v2(*, redis_client: Redis, jti: str, ex) -> bool:
    name = f"token:blacklist:{jti}"
    return redis_client.set(name=name, value=jti, ex=ex)
