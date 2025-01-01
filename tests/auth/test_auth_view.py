import pytest
from fastapi.testclient import TestClient
from src.talentgate.user.models import User
from src.talentgate.user import service as user_service


@pytest.mark.parametrize(
    "user", [{"password": user_service.encode_password("password")}], indirect=True
)
async def test_login(client: TestClient, user: User) -> None:
    response = client.post(
        url="/api/v1/auth/login",
        json={"email": user.email, "password": "password"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


async def test_login_with_invalid_verification(client: TestClient, user: User) -> None:
    user.verified = False

    response = client.post(
        url="/api/v1/auth/login",
        json={"email": user.email, "password": "password"},
    )

    assert response.status_code == 403


@pytest.mark.parametrize(
    "email, password",
    [
        ["invalid_email", "password"],
        ["username@example.com", "invalid_password"],
        ["invalid_email", "invalid_password"],
    ],
)
async def test_login_with_invalid_credentials(
    client: TestClient, user: User, email: str, password: str
) -> None:
    response = client.post(
        url="/api/v1/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 401


async def test_register(client: TestClient) -> None:
    response = client.post(
        url="/api/v1/auth/register",
        json={
            "firstname": "firstname",
            "lastname": "lastname",
            "username": "username",
            "email": "username@example.com",
            "password": "password",
        },
    )

    assert response.status_code == 200
    assert response.json()["username"] == "username"
    assert response.json()["email"] == "username@example.com"
