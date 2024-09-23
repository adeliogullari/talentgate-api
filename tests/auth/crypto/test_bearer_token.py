import pytest
from datetime import datetime, UTC
from src.talentgate.auth.crypto.token import BearerToken


@pytest.mark.parametrize(
    "algorithm, payload, key, headers",
    [
        ("blake2b", {"user_id": 1}, "secret", {"alg": "blake2b", "typ": "JWT"}),
        ("blake2s", {"user_id": 1}, "secret", {"alg": "blake2s", "typ": "JWT"}),
    ],
)
def test_decode(algorithm: str, payload: dict, key: str, headers: dict) -> None:
    bearer_token = BearerToken(algorithm=algorithm)
    token = bearer_token.encode(payload=payload, key=key, headers=headers)
    payload, headers, signature = bearer_token.decode(token=token)

    assert payload["user_id"] == 1
    assert headers["alg"] == algorithm
    assert headers["typ"] == "JWT"
    assert signature is not None


@pytest.mark.parametrize(
    "algorithm, payload, key, headers",
    [
        ("blake2b", {"user_id": 1}, "secret", {"alg": "blake2b", "typ": "JWT"}),
        ("blake2s", {"user_id": 1}, "secret", {"alg": "blake2s", "typ": "JWT"}),
    ],
)
def test_verify(algorithm: str, payload: dict, key: str, headers: dict) -> None:
    bearer_token = BearerToken(algorithm=algorithm)
    token = bearer_token.encode(payload=payload, key=key, headers=headers)
    is_verified = bearer_token.verify(key=key, token=token)
    assert is_verified is True


@pytest.mark.parametrize(
    "algorithm, payload, key, headers",
    [
        ("blake2b", {"user_id": 1}, "secret", {"alg": "blake2b", "typ": "JWT"}),
        ("blake2s", {"user_id": 1}, "secret", {"alg": "blake2s", "typ": "JWT"}),
    ],
)
def test_verify_with_invalid_key(
    algorithm: str, payload: dict, key: str, headers: dict
) -> None:
    bearer_token = BearerToken(algorithm=algorithm)
    token = bearer_token.encode(payload=payload, key=key, headers=headers)
    is_verified = bearer_token.verify(key="invalid_secret", token=token)
    assert is_verified is False


@pytest.mark.parametrize(
    "algorithm, payload, key, headers",
    [
        (
            "blake2b",
            {"exp": datetime.now(UTC).timestamp(), "user_id": 1},
            "secret",
            {"alg": "blake2b", "typ": "JWT"},
        ),
        (
            "blake2s",
            {"exp": datetime.now(UTC).timestamp(), "user_id": 1},
            "secret",
            {"alg": "blake2s", "typ": "JWT"},
        ),
    ],
)
def test_verify_with_exceed_expiration(
    algorithm: str, payload: dict, key: str, headers: dict
) -> None:
    bearer_token = BearerToken(algorithm=algorithm)
    token = bearer_token.encode(
        payload=payload,
        key=key,
        headers=headers,
    )
    is_verified = bearer_token.verify(key=key, token=token)
    assert is_verified is False
