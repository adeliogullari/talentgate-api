from datetime import datetime, timedelta, UTC

from src.talentgate.auth.crypto.token import BearerToken
from src.talentgate.auth.crypto.password.library import PasswordHashLibrary

def encode_password(password: str, algorithm: str, ):
    password_hash_library = PasswordHashLibrary(algorithm=algorithm)

    return password_hash_library.encode(password=password)

def verify_password(password: str, encoded_password: bytes, algorithm: str):
    password_hash_library = PasswordHashLibrary(algorithm=algorithm)

    return password_hash_library.verify(password=password, encoded_password=encoded_password)

def generate_access_token(
    expiration_minutes: float, user_id: int, algorithm: str, key: str
):
    bearer_token = BearerToken(algorithm=algorithm)

    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=expiration_minutes)).timestamp()
    payload = {"exp": exp, "id": user_id}
    headers = {"alg": algorithm, "typ": "JWT"}

    return bearer_token.encode(payload=payload, key=key, headers=headers)


def generate_refresh_token(
    expiration_days: float, user_id: int, algorithm: str, key: str
):
    bearer_token = BearerToken(algorithm=algorithm)

    now = datetime.now(UTC)
    exp = (now + timedelta(days=expiration_days)).timestamp()
    payload = {"exp": exp, "id": user_id}
    headers = {"alg": algorithm, "typ": "JWT"}

    return bearer_token.encode(payload=payload, key=key, headers=headers)
