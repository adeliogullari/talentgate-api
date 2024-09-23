import re
import json
import base64
from typing import Any
from abc import ABC, abstractmethod
from itertools import chain, repeat
from secrets import compare_digest
from src.talentgate.auth.crypto.claims import Payload
from src.talentgate.auth.crypto.digest.library import MessageDigestLibrary


Base64Segment = r"[A-Za-z0-9+/]{4}"
Base64Padding = r"[A-Za-z0-9+/]{2}(?:==)"
Base64OptionalPadding = r"[A-Za-z0-9+/]{3}="
JsonSegment = r"\s*\{.*?}\s*"


class AuthenticationToken(ABC):
    def __init__(self, algorithm: str):
        self.message_digest_library = MessageDigestLibrary(algorithm=algorithm)

    def _is_base64_encoded(self, string: str) -> bool:
        base64_pattern = re.compile(
            f"^(?:{Base64Segment})*(?:{Base64Padding}?|{Base64OptionalPadding})?$"
        )
        return base64_pattern.match(string) is not None

    def _safe_b64encode(self, obj: Any) -> bytes:
        return base64.b64encode(json.dumps(obj).encode())

    def _safe_b64decode(self, string: str) -> bytes:
        if self._is_base64_encoded(string):
            return base64.b64decode(string)
        return base64.b64decode(base64.b64encode(string.encode()))

    def _is_json_serialized(self, string: Any) -> bool:
        json_pattern = re.compile(f"^{JsonSegment}$", re.DOTALL)
        return json_pattern.match(string) is not None

    def _safe_json_loads(self, string: str) -> Any:
        if self._is_json_serialized(string):
            return json.loads(string)
        return json.loads("{}")

    def _verify_signature(self, payload: Any, headers: Any, signature: Any, key: Any):
        token = self.encode(payload=payload, key=key, headers=headers)
        _, _, decoded_signature = self.decode(token=token)
        return compare_digest(signature, decoded_signature)

    @abstractmethod
    def encode(self, payload: Any, key: str, headers: Any) -> str:
        payload = self._safe_b64encode(payload)
        headers = self._safe_b64encode(headers)
        signature = self.message_digest_library.encode(
            data=f"{payload}.{headers}", key=key
        )
        return b".".join([payload, headers, signature]).decode("utf-8")

    @abstractmethod
    def decode(self, token: str) -> tuple[Any, Any, Any]:
        payload, headers, signature, *_ = chain(token.split("."), repeat("{}", 3))
        payload = self._safe_json_loads(self._safe_b64decode(payload).decode("utf-8"))
        headers = self._safe_json_loads(self._safe_b64decode(headers).decode("utf-8"))
        return payload, headers, signature

    @abstractmethod
    def verify(
        self,
        key: str,
        token: str,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
    ) -> bool:
        payload, headers, signature = self.decode(token=token)
        is_payload_verified = Payload(**payload).verify(iss=iss, sub=sub, aud=aud)
        is_signature_verified = self._verify_signature(
            payload=payload, headers=headers, signature=signature, key=key
        )
        return is_payload_verified and is_signature_verified
