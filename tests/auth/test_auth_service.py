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
