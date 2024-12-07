import json
import pytest
from datetime import timedelta, datetime, UTC
from config import Settings
from src.talentgate.auth.crypto.token import BearerToken
from src.talentgate.employee.models import Employee
from src.talentgate.job.models import (
    Job,
    CreateJob,
    UpdateJob,
    EmploymentType,
)
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

from tests.job.conftest import make_job

settings = Settings()


@pytest.fixture
def token(job: Job) -> str:
    access_token = BearerToken("blake2b")

    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "job_id": job.id}
    return access_token.encode(
        payload=payload,
        key=settings.access_token_key,
        headers={"alg": settings.access_token_algorithm, "typ": "JWT"},
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})


async def test_add_observers(
    client: TestClient, job_without_observers: Job, employee: Employee, headers: Headers
) -> None:
    response = client.post(
        url=f"/api/v1/jobs/{job_without_observers.id}/observers",
        headers=headers,
        json=[{"employee_id": employee.id}],
    )

    assert response.status_code == 201
    assert response.json()[0]["employee_id"] == employee.id
    assert response.json()[0]["job_id"] == job_without_observers.id


async def test_retrieve_observers(
    client: TestClient, job: Job, headers: Headers
) -> None:
    response = client.get(url=f"/api/v1/jobs/{job.id}/observers", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["employee_id"] == job.observers[0].id
    assert response.json()[0]["job_id"] == job.id


async def test_delete_observer(
    client: TestClient, job: Job, employee: Employee, headers: Headers
) -> None:
    response = client.delete(
        url=f"/api/v1/jobs/{job.id}/observers/{employee.id}", headers=headers
    )

    assert response.status_code == 200


async def test_create_job(client: TestClient, headers: Headers) -> None:
    created_job = CreateJob(
        title="created job title",
        description="created job description",
        department="created job department",
        employment_type=EmploymentType.FULL_TIME,
        application_deadline=datetime.now(),
    )

    response = client.post(
        url=f"/api/v1/jobs",
        headers=headers,
        json=json.loads(
            created_job.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["title"] == created_job.title
    assert response.json()["description"] == created_job.description
    assert response.json()["department"] == created_job.department
    assert response.json()["employment_type"] == created_job.employment_type


async def test_retrieve_job(client: TestClient, job: Job, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/jobs/{job.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == job.title
    assert response.json()["description"] == job.description
    assert response.json()["department"] == job.department
    assert response.json()["employment_type"] == job.employment_type


async def test_retrieve_jobs(client: TestClient, job: Job, headers: Headers) -> None:
    response = client.get(url="/api/v1/jobs", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["title"] == job.title
    assert response.json()[0]["description"] == job.description
    assert response.json()[0]["department"] == job.department
    assert response.json()[0]["employment_type"] == job.employment_type


async def test_update_job(client: TestClient, job: Job, headers: Headers) -> None:
    updated_job = UpdateJob(
        title="updated job title",
        description="updated job description",
        department="updated job department",
        employment_type=EmploymentType.PART_TIME,
        application_deadline=datetime.now() + timedelta(days=10),
    )

    response = client.put(
        url=f"/api/v1/jobs/{job.id}",
        headers=headers,
        json=json.loads(
            updated_job.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["title"] == updated_job.title
    assert response.json()["description"] == updated_job.description
    assert response.json()["department"] == updated_job.department
    assert response.json()["employment_type"] == updated_job.employment_type


async def test_delete_job(client: TestClient, job: Job, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/jobs/{job.id}", headers=headers)

    assert response.status_code == 200
