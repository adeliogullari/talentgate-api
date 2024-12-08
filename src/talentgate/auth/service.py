from datetime import datetime, timedelta, UTC
from pytography import PasswordHashLibrary, JsonWebToken


def encode_password(
    password: str,
) -> str:
    return PasswordHashLibrary.encode(password=password)


def verify_password(password: str, encoded_password: str) -> bool:
    return PasswordHashLibrary.verify(
        password=password, encoded_password=encoded_password
    )


def generate_access_token(payload: dict, key: str, seconds: float) -> str:
    now = datetime.now(UTC)
    exp = (now + timedelta(seconds=seconds)).timestamp()
    payload.update({"exp": exp})

    return JsonWebToken.encode(payload=payload, key=key)


def generate_refresh_token(payload: dict, key: str, seconds: float) -> str:
    now = datetime.now(UTC)
    exp = (now + timedelta(seconds=seconds)).timestamp()
    payload.update({"exp": exp})

    return JsonWebToken.encode(payload=payload, key=key)


def verify_access_token(token: str, key: str) -> bool:
    return JsonWebToken.verify(token=token, key=key)


def verify_refresh_token(token: str, key: str) -> bool:
    return JsonWebToken.verify(token=token, key=key)
