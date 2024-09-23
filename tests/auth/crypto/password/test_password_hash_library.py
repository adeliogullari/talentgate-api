import pytest
from src.talentgate.auth.crypto.password.library import PasswordHashLibrary


@pytest.mark.parametrize("algorithm", ["pbkdf2", "scrypt"])
@pytest.mark.parametrize("password", ["password"])
def test_verify(algorithm: str, password: str) -> None:
    password_hash_library = PasswordHashLibrary(algorithm=algorithm)
    encoded_password = password_hash_library.encode(password=password)
    is_verified = password_hash_library.verify(
        password=password, encoded_password=encoded_password
    )
    assert is_verified is True


@pytest.mark.parametrize("algorithm", ["pbkdf2", "scrypt"])
@pytest.mark.parametrize("password", ["password"])
def test_verify_with_invalid_input(algorithm: str, password) -> None:
    password_hash_library = PasswordHashLibrary(algorithm=algorithm)
    encoded_password = password_hash_library.encode(password=password)
    is_verified = password_hash_library.verify(
        password="invalid_password", encoded_password=encoded_password
    )
    assert is_verified is False
