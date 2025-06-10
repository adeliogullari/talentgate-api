import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from pytography import JsonWebToken, PasswordHashLibrary
from sqlmodel import Session, select

from src.talentgate.auth.models import TokenBlacklist


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
    payload = {"user_id": user_id, "exp": exp, }
    return JsonWebToken.encode(payload=payload, key=key)


def decode_token(token: str) -> tuple[dict, dict, str]:
    return JsonWebToken.decode(token=token)


def verify_token(token: str, key: str) -> bool:
    return JsonWebToken.verify(token=token, key=key)


def retrieve_refresh_token(
    *, sqlmodel_session: Session, jti: str
) -> TokenBlacklist:
    statement: Any = select(RefreshTokenBlacklist).where(
        RefreshTokenBlacklist.refresh_token == refresh_token,
    )

    return sqlmodel_session.exec(statement).one_or_none()


def revoke_token(
    *, sqlmodel_session: Session, retrieved_refresh_token: RefreshTokenBlacklist
) -> RefreshTokenBlacklist:
    sqlmodel_session.add(retrieved_refresh_token)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_refresh_token)

    return retrieved_refresh_token


def purge_token(
    *, sqlmodel_session: Session, retrieved_refresh_token: RefreshTokenBlacklist
) -> RefreshTokenBlacklist:
    sqlmodel_session.delete(retrieved_refresh_token)
    sqlmodel_session.commit()

    return retrieved_refresh_token
