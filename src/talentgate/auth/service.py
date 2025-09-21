import uuid
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta

from fastapi import BackgroundTasks
from pytography import JsonWebToken, PasswordHashLibrary
from redis import Redis

from src.talentgate.email import service as email_service
from src.talentgate.email.client import EmailClient


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
        "jti": jti,
    }
    return JsonWebToken.encode(payload=payload, key=key)


def decode_token(token: str) -> tuple[dict, dict, str]:
    return JsonWebToken.decode(token=token)


def verify_token(token: str, key: str) -> bool:
    return JsonWebToken.verify(token=token, key=key)


async def blacklist_token(*, redis_client: Redis, jti: str, ex: int) -> bool:
    name = f"token:blacklist:{jti}"
    return await redis_client.set(name=name, value=jti, ex=ex)


async def retrieve_blacklisted_token(*, redis_client: Redis, jti: str | None) -> str | None:
    name = f"token:blacklist:{jti}"
    return await redis_client.get(name=name)


async def send_verification_email(
    *,
    email_client: EmailClient,
    background_tasks: BackgroundTasks,
    context: dict,
    from_addr: str | None = None,
    to_addrs: str | Sequence[str] | None = None,
) -> None:
    body = email_service.load_template(
        file="src/talentgate/auth/templates/verification.txt"
    )

    html = email_service.load_template(
        file="src/talentgate/auth/templates/verification.html"
    )

    background_tasks.add_task(
        email_service.send_email,
        email_client,
        "Email Verification",
        body,
        html,
        context,
        from_addr,
        to_addrs,
    )
