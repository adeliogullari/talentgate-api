import pytest
from src.talentgate.auth.crypto.password.strategy import (
    Pbkdf2PasswordHashStrategy,
    ScryptPasswordHashStrategy,
)


@pytest.mark.parametrize(
    "password_hash_strategy",
    [Pbkdf2PasswordHashStrategy(), ScryptPasswordHashStrategy()],
)
@pytest.mark.parametrize("password", ["password"])
def test_verify(
    password_hash_strategy: Pbkdf2PasswordHashStrategy | ScryptPasswordHashStrategy,
    password,
) -> None:
    encoded_password = password_hash_strategy.encode(password=password)
    is_verified = password_hash_strategy.verify(
        password=password, encoded_password=encoded_password
    )
    assert is_verified is True


@pytest.mark.parametrize(
    "password_hash_strategy",
    [Pbkdf2PasswordHashStrategy(), ScryptPasswordHashStrategy()],
)
@pytest.mark.parametrize("password", ["password"])
def test_verify_with_invalid_input(
    password_hash_strategy: Pbkdf2PasswordHashStrategy | ScryptPasswordHashStrategy,
    password,
) -> None:
    encoded_password = password_hash_strategy.encode(password=password)
    is_verified = password_hash_strategy.verify(
        password="invalid_password", encoded_password=encoded_password
    )
    assert is_verified is False
