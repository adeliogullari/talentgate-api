import json
import uuid
import random
import pytest
from src.talentgate.user.models import (
    User,
    CreateUser,
    UpdateUser,
    UserRole,
    UserSubscription,
)
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

INVALID_ACCESS_TOKEN = uuid.uuid4()
INVALID_USER_ID = random.randint(1, 1000)

invalid_headers = {"Authorization": f"Bearer {INVALID_ACCESS_TOKEN}"}


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_create_user(client: TestClient, headers: Headers) -> None:
    created_user = CreateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        image="image",
        role=UserRole.ACCOUNT_OWNER,
        subscription=UserSubscription.BASIC,
    )

    response = client.post(
        url="/api/v1/users",
        headers=headers,
        json=json.loads(
            created_user.model_dump_json(exclude_unset=True, exclude_none=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["email"] == created_user.email


@pytest.mark.parametrize(
    "user", [{"role": UserRole.ACCOUNT_OWNER}, {"role": UserRole.ADMIN}], indirect=True
)
async def test_retrieve_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_users(client: TestClient, user: User, headers: Headers) -> None:
    response = client.get(url="/api/v1/users", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == user.id


@pytest.mark.parametrize(
    "user", [{"role": UserRole.ACCOUNT_OWNER}, {"role": UserRole.ADMIN}], indirect=True
)
async def test_update_user(client: TestClient, user: User, headers: Headers) -> None:
    updated_user = UpdateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        image="image",
    )

    response = client.put(
        url=f"/api/v1/users/{user.id}",
        headers=headers,
        json=json.loads(
            updated_user.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["email"] == updated_user.email


@pytest.mark.parametrize(
    "user", [{"role": UserRole.ACCOUNT_OWNER}, {"role": UserRole.ADMIN}], indirect=True
)
async def test_delete_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
