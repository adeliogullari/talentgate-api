import json
import uuid
import random
import pytest
from datetime import timedelta, datetime, UTC
from config import Settings
from src.talentgate.auth.crypto.token import BearerToken
from src.talentgate.user.models import User, CreateUser, UserRole, UserSubscription, UpdateUser
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


async def test_create_user(client: TestClient, headers: Headers) -> None:
    created_user = CreateUser(
        firstname="created firstname",
        lastname="created lastname",
        username="created username",
        email="created_email@gmail.com",
        password="createdPassword",
        verified=True,
        image="created/image",
        role=UserRole.ACCOUNT_OWNER,
        subscription=UserSubscription.BASIC
    )

    response = client.post(url=f"/api/v1/users", headers=headers, json=json.loads(created_user.model_dump_json(exclude_unset=True, exclude_none=True)))

    assert response.status_code == 201
    assert response.json()["firstname"] == created_user.firstname


async def test_retrieve_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_retrieve_users(client: TestClient, user: User, headers: Headers) -> None:
    response = client.get(url="/api/v1/users", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == user.id


async def test_update_user(client: TestClient, user: User, headers: Headers) -> None:
    updated_user = UpdateUser(
        firstname="updated firstname",
        lastname="updated lastname",
        username="updated username",
        email="updated_email@gmail.com",
        password="updatedPassword",
        verified=True,
        image="updated/image",
        role=UserRole.ACCOUNT_OWNER,
        subscription=UserSubscription.BASIC
    )

    response = client.put(url=f"/api/v1/users/{user.id}", headers=headers, json=json.loads(updated_user.model_dump_json(exclude_none=True, exclude_unset=True)))

    assert response.status_code == 200
    assert response.json()["firstname"] == updated_user.firstname


async def test_delete_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
