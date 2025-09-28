import pytest
from starlette.datastructures import Headers

from src.talentgate.auth import service as auth_service


@pytest.fixture
def access_token(user, settings, request) -> str:
    param = getattr(request, "param", {})
    user_id = param.get("user_id", str(user.id))
    key = param.get("key", settings.access_token_key)
    seconds = param.get("seconds", settings.access_token_expiration)

    return auth_service.encode_token(
        user_id=user_id,
        key=key,
        seconds=seconds,
    )


@pytest.fixture
def refresh_token(user, settings, request) -> str:
    param = getattr(request, "param", {})
    user_id = param.get("user_id", str(user.id))
    key = param.get("key", settings.refresh_token_key)
    seconds = param.get("seconds", settings.refresh_token_expiration)

    return auth_service.encode_token(
        user_id=user_id,
        key=key,
        seconds=seconds,
    )


@pytest.fixture
def headers(access_token) -> Headers:
    return Headers({"Authorization": f"Bearer {access_token}"})
