import uuid
import random
import pytest
from datetime import timedelta, datetime, UTC
from config import Settings
from src.talentgate.auth.crypto.token import BearerToken
from src.talentgate.user.models import User
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

settings = Settings()


INVALID_ACCESS_TOKEN = uuid.uuid4()
INVALID_USER_ID = random.randint(1, 1000)

invalid_headers = {"Authorization": f"Bearer {INVALID_ACCESS_TOKEN}"}


@pytest.fixture
def token(user: User) -> str:
    access_token = BearerToken("blake2b")

    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "user_id": user.id}
    return access_token.encode(
        payload=payload,
        key=settings.access_token_key,
        headers={"alg": settings.access_token_algorithm, "typ": "JWT"},
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})


async def test_create_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_retrieve_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_retrieve_users(client: TestClient, user: User, headers: Headers) -> None:
    response = client.get(url="/api/v1/users", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == user.id
