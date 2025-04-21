import pytest
from starlette.datastructures import Headers

from config import get_settings
from src.talentgate.auth import service as auth_service

settings = get_settings()


@pytest.fixture
def access_token(user):
    return auth_service.encode_token(
        user_id=str(user.id),
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )


@pytest.fixture
def refresh_token(user):
    return auth_service.encode_token(
        user_id=str(user.id),
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )


@pytest.fixture
def headers(access_token) -> Headers:
    return Headers({"Authorization": f"Bearer {access_token}"})
