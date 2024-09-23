import json
import base64
import hashlib
import secrets
from typing import Any
from src.talentgate.auth.crypto.password.abstract import PasswordHashAlgorithm


class Pbkdf2(PasswordHashAlgorithm):
    algorithm = "pbkdf2"
    hash_name = "sha256"
    iterations = 600000
    dklen = 64

    def encode(self, password: str, salt: str = secrets.token_hex(64)) -> bytes:
        password_hash = hashlib.pbkdf2_hmac(
            hash_name=self.hash_name,
            password=password.encode("utf-8"),
            salt=salt.encode("utf-8"),
            iterations=self.iterations,
            dklen=self.dklen,
        )

        return base64.b64encode(
            json.dumps(
                {
                    "algorithm": self.algorithm,
                    "hash_name": self.hash_name,
                    "password_hash": base64.b64encode(password_hash).decode("utf-8"),
                    "salt": salt,
                    "iterations": self.iterations,
                    "dklen": self.dklen,
                }
            ).encode("utf-8")
        )

    def decode(self, encoded_password: bytes) -> Any:
        return super().decode(encoded_password=encoded_password)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return super().verify(password=password, encoded_password=encoded_password)


class Scrypt(PasswordHashAlgorithm):
    algorithm = "scrypt"
    cost_factor = 2**14
    block_size = 8
    parallelization_factor = 1
    maxmem = 0
    dklen = 64

    def encode(self, password: str, salt: str = secrets.token_hex(64)) -> bytes:
        password_hash = hashlib.scrypt(
            password=password.encode("utf-8"),
            salt=salt.encode("utf-8"),
            n=self.cost_factor,
            r=self.block_size,
            p=self.parallelization_factor,
            maxmem=self.maxmem,
            dklen=self.dklen,
        )

        return base64.b64encode(
            json.dumps(
                {
                    "algorithm": self.algorithm,
                    "password_hash": base64.b64encode(password_hash).decode("utf-8"),
                    "salt": salt,
                    "cost_factor": self.cost_factor,
                    "block_size": self.block_size,
                    "parallelization_factor": self.parallelization_factor,
                    "maxmem": self.maxmem,
                    "dklen": self.dklen,
                }
            ).encode("utf-8")
        )

    def decode(self, encoded_password: bytes) -> Any:
        return super().decode(encoded_password=encoded_password)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return super().verify(password=password, encoded_password=encoded_password)
