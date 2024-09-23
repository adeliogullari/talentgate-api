import pytest
from src.talentgate.auth.crypto.digest.strategy import (
    Blake2bMessageDigestStrategy,
    Blake2sMessageDigestStrategy,
)


@pytest.mark.parametrize(
    "message_digest_strategy",
    [Blake2bMessageDigestStrategy(), Blake2sMessageDigestStrategy()],
)
@pytest.mark.parametrize("data, key", [("message", "secret")])
def test_verify(
    message_digest_strategy: Blake2bMessageDigestStrategy
    | Blake2sMessageDigestStrategy,
    data: str,
    key: str,
) -> None:
    encoded_data = message_digest_strategy.encode(data=data, key=key)
    is_verified = message_digest_strategy.verify(
        data=data, key=key, encoded_data=encoded_data
    )
    assert is_verified is True


@pytest.mark.parametrize(
    "message_digest_strategy",
    [Blake2bMessageDigestStrategy(), Blake2sMessageDigestStrategy()],
)
@pytest.mark.parametrize(
    "data, key", [("invalid_message", "secret"), ("message", "invalid_secret")]
)
def test_verify_with_invalid_input(
    message_digest_strategy: Blake2bMessageDigestStrategy
    | Blake2sMessageDigestStrategy,
    data: str,
    key: str,
) -> None:
    encoded_data = message_digest_strategy.encode(data="message", key="secret")
    is_verified = message_digest_strategy.verify(
        data=data, key=key, encoded_data=encoded_data
    )
    assert is_verified is False
