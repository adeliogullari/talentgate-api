import json
import base64
import secrets
from typing import Any
from hashlib import blake2s, blake2b
from src.talentgate.auth.crypto.digest.absctract import MessageDigestAlgorithm


class Blake2b(MessageDigestAlgorithm):
    algorithm = "blake2b"
    digest_size = blake2b.MAX_DIGEST_SIZE

    def encode(
        self,
        data: str,
        key: str = secrets.token_hex(16),
        salt: str = secrets.token_hex(4),
    ) -> bytes:
        data_hash = blake2b(
            data.encode("utf-8"),
            digest_size=self.digest_size,
            key=key.encode("utf-8"),
            salt=salt.encode("utf-8"),
        ).digest()

        return base64.b64encode(
            json.dumps(
                {
                    "algorithm": self.algorithm,
                    "data_hash": base64.b64encode(data_hash).decode("utf-8"),
                    "salt": salt,
                    "digest_size": self.digest_size,
                }
            ).encode("utf-8")
        )

    def decode(self, encoded_data: bytes) -> Any:
        return super().decode(encoded_data=encoded_data)

    def verify(self, data: str, key: str, encoded_data: bytes) -> bool:
        return super().verify(data=data, key=key, encoded_data=encoded_data)


class Blake2s(MessageDigestAlgorithm):
    algorithm = "blake2s"
    digest_size = blake2s.MAX_DIGEST_SIZE

    def encode(
        self,
        data: str,
        key: str = secrets.token_hex(16),
        salt: str = secrets.token_hex(4),
    ) -> bytes:
        data_hash = blake2s(
            data.encode("utf-8"),
            digest_size=self.digest_size,
            key=key.encode("utf-8"),
            salt=salt.encode("utf-8"),
        ).digest()

        return base64.b64encode(
            json.dumps(
                {
                    "algorithm": self.algorithm,
                    "data_hash": base64.b64encode(data_hash).decode("utf-8"),
                    "salt": salt,
                    "digest_size": self.digest_size,
                }
            ).encode("utf-8")
        )

    def decode(self, encoded_data: bytes) -> Any:
        return super().decode(encoded_data=encoded_data)

    def verify(self, data: str, key: str, encoded_data: bytes) -> bool:
        return super().verify(data=data, key=key, encoded_data=encoded_data)
