import uuid

import pytest
from redis import Redis

from config import Settings
from src.talentgate.auth import service as auth_service
from src.talentgate.user.models import User


async def test_verify_access_token(
    user: User, access_token: str, settings: Settings
) -> None:
    is_verified = auth_service.verify_token(
        token=access_token, key=settings.access_token_key
    )

    assert is_verified == True


@pytest.mark.parametrize(
    "access_token",
    [
        {
            "key": "invalid_key",
        }
    ],
    indirect=True,
)
async def test_verify_invalid_access_token(
    user: User, access_token: str, settings: Settings
) -> None:
    is_verified = auth_service.verify_token(
        token=access_token, key=settings.access_token_key
    )

    assert is_verified == False


async def test_verify_refresh_token(
    user: User, refresh_token: str, settings: Settings
) -> None:
    is_verified = auth_service.verify_token(
        token=refresh_token, key=settings.refresh_token_key
    )

    assert is_verified == True


@pytest.mark.parametrize(
    "refresh_token",
    [
        {
            "key": "invalid_key",
        }
    ],
    indirect=True,
)
async def test_verify_invalid_refresh_token(
    user: User, refresh_token: str, settings: Settings
) -> None:
    is_verified = auth_service.verify_token(
        token=refresh_token, key=settings.refresh_token_key
    )

    assert is_verified == False


async def test_blacklist_token(redis_client: Redis, settings: Settings) -> None:
    jti = str(uuid.uuid4())
    await auth_service.blacklist_token(
        redis_client=redis_client, jti=jti, ex=int(settings.refresh_token_expiration)
    )
    retrieved_token = await redis_client.get(name=f"token:blacklist:{jti}")
    assert retrieved_token == jti


async def test_retrieve_blacklisted_token(redis_client: Redis) -> None:
    jti = str(uuid.uuid4())
    await redis_client.set(name=f"token:blacklist:{jti}", value=jti)
    retrieved_token = await auth_service.retrieve_blacklisted_token(
        redis_client=redis_client, jti=jti
    )
    assert retrieved_token == jti
