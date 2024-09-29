import pytest
from fastapi.testclient import TestClient
from src.talentgate.user.models import User
from src.talentgate.auth.crypto.password.library import PasswordHashLibrary

password_hash_library = PasswordHashLibrary("scrypt")


async def test_login(client: TestClient, user: User) -> None:
    response = client.post(
        url="/api/v1/auth/login",
        json={"email": user.email, "password": "secret"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None
