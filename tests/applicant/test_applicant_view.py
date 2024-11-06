import uuid
import random
import pytest
from datetime import timedelta, datetime, UTC
from config import Settings
from src.talentgate.auth.crypto.token import BearerToken
from src.talentgate.applicant.models import Applicant
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

settings = Settings()


INVALID_ACCESS_TOKEN = uuid.uuid4()
INVALID_APPLICANT_ID = random.randint(1, 1000)

invalid_headers = {"Authorization": f"Bearer {INVALID_ACCESS_TOKEN}"}


@pytest.fixture
def token(applicant: Applicant) -> str:
    access_token = BearerToken("blake2b")

    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "applicant_id": applicant.id}
    return access_token.encode(
        payload=payload,
        key=settings.access_token_key,
        headers={"alg": settings.access_token_algorithm, "typ": "JWT"},
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})


async def test_create_applicant(client: TestClient, applicant: Applicant, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/applicant/{applicant.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == applicant.id


async def test_retrieve_applicant(client: TestClient, applicant: Applicant, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/applicant/{applicant.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == applicant.id


async def test_retrieve_applicants(client: TestClient, applicant: Applicant, headers: Headers) -> None:
    response = client.get(url="/api/v1/applicant", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == applicant.id
