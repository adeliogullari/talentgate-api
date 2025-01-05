import json
import pytest
from src.talentgate.user.models import (
    User,
    UserRole,
    CreateUser,
    UpdateUser,
    UpdateCurrentUser,
)
from starlette.datastructures import Headers
from fastapi.testclient import TestClient


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_create_user(client: TestClient, headers: Headers) -> None:
    created_user = CreateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ACCOUNT_OWNER,
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


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_retrieve_current_user(
    client: TestClient, user, headers: Headers
) -> None:
    response = client.get(url=f"/api/v1/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_users(client: TestClient, user: User, headers: Headers) -> None:
    params = {
        "offset": 0,
        "limit": 100,
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "username": user.username,
        "email": user.email,
        "verified": user.verified,
        "role": user.role,
    }

    response = client.get(url="/api/v1/users", params=params, headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == user.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_update_user(client: TestClient, user: User, headers: Headers) -> None:
    updated_user = UpdateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        verified=True,
        role=UserRole.ACCOUNT_OWNER,
    )

    response = client.patch(
        url=f"/api/v1/users/{user.id}",
        headers=headers,
        json=json.loads(
            updated_user.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["email"] == updated_user.email


async def test_update_current_user(
    client: TestClient, user: User, headers: Headers
) -> None:
    updated_user = UpdateCurrentUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
    )

    response = client.patch(
        url=f"/api/v1/me",
        headers=headers,
        json=json.loads(
            updated_user.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["email"] == updated_user.email


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_delete_user(client: TestClient, user: User, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/users/{user.id}", headers=headers)

    assert response.status_code == 200


async def test_delete_current_user(client: TestClient, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/me", headers=headers)

    assert response.status_code == 200
