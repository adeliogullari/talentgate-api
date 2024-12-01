import json
import pytest
from datetime import timedelta, datetime, UTC
from config import Settings
from src.talentgate.auth.crypto.token import BearerToken
from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job
from src.talentgate.observer.models import (
    Observer,
    CreateObserver,
)
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

settings = Settings()


@pytest.fixture
def token(observer: Observer) -> str:
    access_token = BearerToken("blake2b")

    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "observer_id": observer.id}
    return access_token.encode(
        payload=payload,
        key=settings.access_token_key,
        headers={"alg": settings.access_token_algorithm, "typ": "JWT"},
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})


async def test_create_observer(client: TestClient, headers: Headers) -> None:
    created_observer = CreateObserver(
        job_id=1,
        employee_id=1,
    )

    response = client.post(
        url="/api/v1/observers",
        headers=headers,
        json=json.loads(
            created_observer.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["employee_id"] == created_observer.employee_id
    assert response.json()["job_id"] == created_observer.job_id


async def test_retrieve_observer(
    client: TestClient, observer: Observer, headers: Headers
) -> None:
    response = client.get(url=f"/api/v1/observers/{observer.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["employee_id"] == observer.employee_id
    assert response.json()["job_id"] == observer.job_id


async def test_retrieve_observers_of_single_job(
    client: TestClient,
    observer: Observer,
    headers: Headers,
    job: Job,
    employee: Employee,
) -> None:
    response = client.get(url=f"/api/v1/jobs/{job.id}/observers", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["employee_id"] == observer.employee_id
    assert response.json()[0]["job_id"] == observer.job_id


# TODO: Bu teste ve update metoduna ihtiyaç var mı?
# async def test_update_observer(client: TestClient, observer: Observer, headers: Headers) -> None:
#     updated_observer = UpdateObserver(
#         job_id=2,
#         employee_id=2,
#     )
#
#     response = client.put(
#         url=f"/api/v1/observers/{observer.id}",
#         headers=headers,
#         json=json.loads(
#             updated_observer.model_dump_json(exclude_none=True, exclude_unset=True)
#         ),
#     )
#
#     assert response.status_code == 409


async def test_delete_observer(
    client: TestClient, observer: Observer, headers: Headers
) -> None:
    response = client.delete(url=f"/api/v1/observers/{observer.id}", headers=headers)

    assert response.status_code == 200
