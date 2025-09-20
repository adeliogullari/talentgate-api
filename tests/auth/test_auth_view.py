import pytest
from fastapi.testclient import TestClient
from starlette.datastructures import Headers

from src.talentgate.auth import service as auth_service
from src.talentgate.user.enums import SubscriptionPlan, SubscriptionStatus
from src.talentgate.user.models import User


@pytest.mark.parametrize(
    "user",
    [{"password": auth_service.encode_password("password")}],
    indirect=True,
)
async def test_login(client: TestClient, user: User) -> None:
    response = client.post(
        url="/api/v1/auth/login",
        json={"email": user.email, "password": "password"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


@pytest.mark.parametrize(
    "user",
    [{"password": auth_service.encode_password("password"), "verified": False}],
    indirect=True,
)
async def test_login_with_invalid_verification(client: TestClient, user: User) -> None:
    response = client.post(
        url="/api/v1/auth/login",
        json={"email": user.email, "password": "password"},
    )

    assert response.status_code == 403


@pytest.mark.parametrize(
    "user",
    [
        {
            "email": "username@example.com",
            "password": auth_service.encode_password("password"),
        }
    ],
    indirect=True,
)
@pytest.mark.parametrize(
    "email, password",
    [
        ["invalid_email", "password"],
        ["username@example.com", "invalid_password"],
        ["invalid_email", "invalid_password"],
    ],
)
async def test_login_with_invalid_credentials(
    client: TestClient,
    user: User,
    email: str,
    password: str,
) -> None:
    response = client.post(
        url="/api/v1/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "firstname, lastname, username, email, password",
    [
        ["firstname", "lastname", "username", "username@example.com", "password"],
    ],
)
async def test_register(
    client: TestClient,
    firstname: str,
    lastname: str,
    username: str,
    email: str,
    password: str,
) -> None:
    response = client.post(
        url="/api/v1/auth/register",
        json={
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == email
    assert response.json()["subscription"]["plan"] == SubscriptionPlan.STANDARD
    assert response.json()["subscription"]["status"] == SubscriptionStatus.ACTIVE


@pytest.mark.parametrize(
    "user",
    [
        {
            "username": "username",
            "email": "username@example.com",
        },
    ],
    indirect=True,
)
@pytest.mark.parametrize(
    "username, email",
    [
        ["username", "unique_username@example.com"],
        ["unique_username", "username@example.com"],
        ["username", "username@example.com"],
    ],
)
async def test_register_with_existing_user(
    client: TestClient, user: User, username: str, email: str
) -> None:
    response = client.post(
        url="/api/v1/auth/register",
        json={
            "firstname": "firstname",
            "lastname": "lastname",
            "username": username,
            "email": email,
            "password": "password",
        },
    )

    assert response.status_code == 409


@pytest.mark.parametrize(
    "user",
    [
        {
            "verified": False,
        },
    ],
    indirect=True,
)
async def test_verify_email(client: TestClient, user: User, headers: Headers) -> None:
    response = client.post(url="/api/v1/auth/email/verify", headers=headers)

    assert response.status_code == 200


async def test_verify_email_already_verified(
    client: TestClient, user: User, headers: Headers
) -> None:
    response = client.post(url="/api/v1/auth/email/verify", headers=headers)

    assert response.status_code == 400


@pytest.mark.parametrize(
    "user",
    [
        {
            "verified": False,
        },
    ],
    indirect=True,
)
async def test_resend_email(
    client: TestClient,
    user: User,
) -> None:
    response = client.post(
        url="/api/v1/auth/email/verify/resend",
        json={
            "email": user.email,
        },
    )

    assert response.status_code == 200


async def test_resend_email_already_verified(client: TestClient, user: User) -> None:
    response = client.post(
        url="/api/v1/auth/email/verify/resend",
        json={
            "email": user.email,
        },
    )

    assert response.status_code == 400


async def test_refresh_token(
    client: TestClient, user: User, headers: Headers, refresh_token: str
) -> None:
    client.cookies.set("refresh_token", refresh_token)
    response = client.post(
        url="/api/v1/auth/token/refresh",
        json={"refresh_token": refresh_token},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None


@pytest.mark.parametrize(
    "refresh_token",
    [
        {
            "key": "invalid_key",
        },
    ],
    indirect=True,
)
async def test_refresh_invalid_token(
    client: TestClient, user: User, headers: Headers, refresh_token: str
) -> None:
    client.cookies.set("refresh_token", refresh_token)
    response = client.post(
        url="/api/v1/auth/token/refresh",
        json={"refresh_token": refresh_token},
        headers=headers,
    )

    assert response.status_code == 401


async def test_logout(
    client: TestClient,
    user: User,
    headers: Headers,
    access_token: str,
    refresh_token: str,
) -> None:
    client.cookies.set("access_token", access_token)
    client.cookies.set("refresh_token", refresh_token)

    response = client.post(
        url="/api/v1/auth/logout",
        json={"refresh_token": refresh_token},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None


async def test_logout_with_invalid_refresh_token(
    client: TestClient,
    user: User,
    headers: Headers,
    access_token: str,
    refresh_token: str,
) -> None:
    client.cookies.set("access_token", access_token)
    client.cookies.set("refresh_token", refresh_token)

    response = client.post(
        url="/api/v1/auth/logout",
        json={"refresh_token": refresh_token},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None
