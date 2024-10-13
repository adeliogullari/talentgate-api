from datetime import datetime, timedelta, UTC

from src.talentgate.auth.crypto.token import BearerToken


def generate_access_token(expiration_minutes: float, user_id: int, algorithm: str, key: str):
    bearer_token = BearerToken(algorithm=algorithm)

    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=expiration_minutes)).timestamp()
    payload = {"exp": exp, "id": user_id}
    headers = {"alg": algorithm, "typ": 'JWT'}

    return bearer_token.encode(payload=payload, key=key, headers=headers)


def generate_refresh_token(expiration_days: float, user_id: int, algorithm: str, key: str):
    bearer_token = BearerToken(algorithm=algorithm)

    now = datetime.now(UTC)
    exp = (now + timedelta(days=expiration_days)).timestamp()
    payload = {"exp": exp, "id": user_id}
    headers = {"alg": algorithm, "typ": 'JWT'}

    return bearer_token.encode(payload=payload, key=key, headers=headers)
