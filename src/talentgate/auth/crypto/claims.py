from uuid import uuid4
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC


def default_exp() -> float:
    now = datetime.now(UTC)
    return (now + timedelta(seconds=7200)).timestamp()


def default_nbf() -> float:
    now = datetime.now(UTC)
    return (now - timedelta(seconds=120)).timestamp()


def default_iat() -> float:
    now = datetime.now(UTC)
    return (now - timedelta(seconds=120)).timestamp()


def default_jti() -> str:
    return uuid4().hex


@dataclass
class RegisteredClaims:
    iss: str | None = None
    sub: str | None = None
    aud: str | None = None
    exp: float = field(default_factory=default_exp)
    nbf: float = field(default_factory=default_nbf)
    iat: float = field(default_factory=default_iat)
    jti: str = field(default_factory=default_jti)

    def _is_iss_verified(self, iss: str | None) -> bool:
        return self.iss == iss

    def _is_sub_verified(self, sub: str | None) -> bool:
        return self.sub == sub

    def _is_aud_verified(self, aud: str | None) -> bool:
        return self.aud == aud

    def _is_exp_verified(self, now: float) -> bool:
        return now < self.exp

    def _is_nbf_verified(self, now: float) -> bool:
        return self.nbf < now

    def _is_iat_verified(self, now: float) -> bool:
        return self.iat < now

    def verify(
        self, iss: str | None = None, sub: str | None = None, aud: str | None = None
    ) -> bool:
        now = datetime.now(UTC).timestamp()
        is_iss_verified = self._is_iss_verified(iss=iss)
        is_sub_verified = self._is_sub_verified(sub=sub)
        is_aud_verified = self._is_aud_verified(aud=aud)
        is_exp_verified = self._is_exp_verified(now=now)
        is_nbf_verified = self._is_nbf_verified(now=now)
        is_iat_verified = self._is_iat_verified(now=now)
        return (
            is_iss_verified
            and is_sub_verified
            and is_aud_verified
            and is_exp_verified
            and is_nbf_verified
            and is_iat_verified
        )


@dataclass
class CustomClaims:
    user_id: str | None = None


@dataclass
class PublicClaims:
    auth_time: float | None = None
    acr: float | None = None
    nonce: float | None = None


@dataclass
class PrivateClaims:
    pass


@dataclass
class Payload(RegisteredClaims, CustomClaims, PublicClaims, PrivateClaims):
    pass
