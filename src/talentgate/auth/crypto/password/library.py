from src.talentgate.auth.crypto.password.factory import PasswordHashStrategyFactory


class PasswordHashLibrary:
    def __init__(self, algorithm: str):
        self._strategy = PasswordHashStrategyFactory.create(algorithm=algorithm)

    def encode(self, password: str) -> bytes:
        return self._strategy.encode(password=password)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return self._strategy.verify(
            password=password, encoded_password=encoded_password
        )
