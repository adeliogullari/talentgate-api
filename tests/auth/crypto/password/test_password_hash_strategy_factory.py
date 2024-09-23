import pytest
from src.talentgate.auth.crypto.password.factory import PasswordHashStrategyFactory


@pytest.mark.parametrize("algorithm", ["blake2b", "blake2s"])
@pytest.mark.parametrize("password", ["password"])
def test_verify(algorithm: str, password: str) -> None:
    password_hash_strategy_factory = PasswordHashStrategyFactory.create(
        algorithm=algorithm
    )
    encoded_password = password_hash_strategy_factory.encode(password=password)
    is_verified = password_hash_strategy_factory.verify(
        password=password, encoded_password=encoded_password
    )
    assert is_verified is True


@pytest.mark.parametrize("algorithm", ["blake2b", "blake2s"])
@pytest.mark.parametrize("password", ["password"])
def test_verify_with_invalid_input(algorithm: str, password: str) -> None:
    password_hash_strategy_factory = PasswordHashStrategyFactory.create(
        algorithm=algorithm
    )
    encoded_password = password_hash_strategy_factory.encode(password=password)
    is_verified = password_hash_strategy_factory.verify(
        password="invalid_password", encoded_password=encoded_password
    )
    assert is_verified is False
