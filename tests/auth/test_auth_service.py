import uuid

from redis import Redis

from config import get_settings
from src.talentgate.auth import service as auth_service
from src.talentgate.user.models import User

settings = get_settings()


async def test_verify_access_token(user: User) -> None:
    token = auth_service.encode_token(
        user_id=str(user.id),
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    is_verified = auth_service.verify_token(token=token, key=settings.access_token_key)

    assert is_verified == True


async def test_verify_refresh_token(user: User) -> None:
    token = auth_service.encode_token(
        user_id=str(user.id),
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    is_verified = auth_service.verify_token(token=token, key=settings.refresh_token_key)

    assert is_verified == True


async def test_blacklist_token(redis_client: Redis) -> None:
    jti = str(uuid.uuid4())
    await auth_service.blacklist_token(redis_client=redis_client, jti=jti, ex=86400)
    retrieved_token = await redis_client.get(name=f"token:blacklist:{jti}")
    assert retrieved_token == jti


async def test_retrieve_blacklisted_token(redis_client: Redis) -> None:
    jti = str(uuid.uuid4())
    await redis_client.set(name=f"token:blacklist:{jti}", value=jti)
    retrieved_token = await auth_service.retrieve_blacklisted_token(
        redis_client=redis_client, jti=jti
    )
    assert retrieved_token == jti
