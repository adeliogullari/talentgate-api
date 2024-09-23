from src.talentgate.auth.crypto.password.algorithm import Pbkdf2, Scrypt
from src.talentgate.auth.crypto.password.abstract import PasswordHashStrategy


class Pbkdf2PasswordHashStrategy(PasswordHashStrategy):
    def __init__(self) -> None:
        self.pbkdf2 = Pbkdf2()

    def encode(self, password: str) -> bytes:
        return self.pbkdf2.encode(password=password)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return self.pbkdf2.verify(password=password, encoded_password=encoded_password)


class ScryptPasswordHashStrategy(PasswordHashStrategy):
    def __init__(self) -> None:
        self.scrypt = Scrypt()

    def encode(self, password: str) -> bytes:
        return self.scrypt.encode(password=password)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return self.scrypt.verify(password=password, encoded_password=encoded_password)
