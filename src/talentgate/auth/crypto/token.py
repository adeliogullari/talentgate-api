from typing import Any
from .abstract import AuthenticationToken


class BearerToken(AuthenticationToken):
    def encode(self, payload: Any, key: str, headers: Any) -> str:
        return super().encode(payload=payload, key=key, headers=headers)

    def decode(self, token: str) -> tuple[Any, Any, Any]:
        return super().decode(token=token)

    def verify(
        self,
        key: str,
        token: str,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
    ) -> bool:
        return super().verify(key=key, token=token, iss=iss, sub=sub, aud=aud)
