import json
import pytest
from datetime import timedelta, datetime, UTC
from config import Settings
from src.talentgate.company.models import Company
from src.talentgate.job.models import (
    Job,
    CreateJob,
    UpdateJob,
    EmploymentType,
)
from pytography import JsonWebToken
from starlette.datastructures import Headers
from fastapi.testclient import TestClient


settings = Settings()


@pytest.fixture
def token(job: Job) -> str:
    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "job_id": job.id}
    return JsonWebToken.encode(
        payload=payload,
        key=settings.access_token_key,
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})


async def test_create_job(
    client: TestClient, headers: Headers, company: Company
) -> None:
    created_job = CreateJob(
        title="created job title",
        description="created job description",
        department="created job department",
        employment_type=EmploymentType.FULL_TIME,
        application_deadline=datetime.now(),
        company_id=company.id,
    )

    response = client.post(
        url="/api/v1/jobs",
        headers=headers,
        json=json.loads(
            created_job.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["title"] == created_job.title
    assert response.json()["department"] == created_job.department
    assert response.json()["employment_type"] == created_job.employment_type


async def test_retrieve_job(client: TestClient, job: Job, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/jobs/{job.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == job.title
    assert response.json()["department"] == job.department
    assert response.json()["employment_type"] == job.employment_type


async def test_retrieve_jobs(client: TestClient, job: Job, headers: Headers) -> None:
    response = client.get(url="/api/v1/jobs", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["title"] == job.title
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
    assert response.json()["department"] == updated_job.department
    assert response.json()["employment_type"] == updated_job.employment_type


async def test_delete_job(client: TestClient, job: Job, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/jobs/{job.id}", headers=headers)

    assert response.status_code == 200
