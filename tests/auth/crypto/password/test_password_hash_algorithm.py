import pytest
from src.talentgate.auth.crypto.password.algorithm import Pbkdf2, Scrypt


@pytest.mark.parametrize("password_hash_algorithm", [Pbkdf2(), Scrypt()])
@pytest.mark.parametrize("password", ["password"])
def test_verify(password_hash_algorithm: Pbkdf2 | Scrypt, password: str) -> None:
    encoded_password = password_hash_algorithm.encode(password=password)
    is_verified = password_hash_algorithm.verify(
        password=password, encoded_password=encoded_password
    )
    assert is_verified is True


@pytest.mark.parametrize("password_hash_algorithm", [Pbkdf2(), Scrypt()])
@pytest.mark.parametrize("password", ["password"])
def test_verify_with_invalid_input(
    password_hash_algorithm: Pbkdf2 | Scrypt, password: str
) -> None:
    encoded_password = password_hash_algorithm.encode(password=password)
    is_verified = password_hash_algorithm.verify(
        password="invalid_password", encoded_password=encoded_password
    )
    assert is_verified is False
