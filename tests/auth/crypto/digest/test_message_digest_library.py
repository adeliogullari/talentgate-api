import pytest
from src.talentgate.auth.crypto.digest.library import MessageDigestLibrary


@pytest.mark.parametrize("algorithm", ["blake2b", "blake2s"])
@pytest.mark.parametrize("data, key", [("message", "secret")])
def test_verify(algorithm: str, data: str, key: str) -> None:
    message_digest_library = MessageDigestLibrary(algorithm=algorithm)
    encoded_data = message_digest_library.encode(data=data, key=key)
    is_verified = message_digest_library.verify(
        data=data, key=key, encoded_data=encoded_data
    )
    assert is_verified is True


@pytest.mark.parametrize("algorithm", ["blake2b", "blake2s"])
@pytest.mark.parametrize(
    "data, key", [("invalid_message", "secret"), ("message", "invalid_secret")]
)
def test_verify_with_invalid_input(algorithm: str, data: str, key: str) -> None:
    message_digest_library = MessageDigestLibrary(algorithm=algorithm)
    encoded_data = message_digest_library.encode(data="message", key="secret")
    is_verified = message_digest_library.verify(
        data=data, key=key, encoded_data=encoded_data
    )
    assert is_verified is False
