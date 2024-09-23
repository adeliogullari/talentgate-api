import secrets
from src.talentgate.auth.crypto.digest.algorithm import Blake2s, Blake2b
from src.talentgate.auth.crypto.digest.absctract import MessageDigestStrategy


class Blake2bMessageDigestStrategy(MessageDigestStrategy):
    def __init__(self) -> None:
        self.blake2b = Blake2b()

    def encode(
        self,
        data: str,
        key: str = secrets.token_hex(16),
    ) -> bytes:
        return self.blake2b.encode(data=data, key=key)

    def verify(self, data: str, key: str, encoded_data: bytes) -> bool:
        return self.blake2b.verify(data=data, key=key, encoded_data=encoded_data)


class Blake2sMessageDigestStrategy(MessageDigestStrategy):
    def __init__(self) -> None:
        self.blake2s = Blake2s()

    def encode(
        self,
        data: str,
        key: str = secrets.token_hex(16),
    ) -> bytes:
        return self.blake2s.encode(data=data, key=key)

    def verify(self, data: str, key: str, encoded_data: bytes) -> bool:
        return self.blake2s.verify(data=data, key=key, encoded_data=encoded_data)
