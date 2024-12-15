from datetime import datetime, timedelta, UTC
from pytography import JsonWebToken


def encode_token(user_id: str, key: str, seconds: float) -> str:
    now = datetime.now(UTC)
    exp = (now + timedelta(seconds=seconds)).timestamp()
    payload = {"user_id": user_id, "exp": exp}
    return JsonWebToken.encode(payload=payload, key=key)


def verify_token(token: str, key: str) -> bool:
    return JsonWebToken.verify(token=token, key=key)
