import json
from datetime import datetime, UTC, timedelta

import pytest
from pytography import JsonWebToken

from config import Settings
from src.talentgate.company.models import Company, CreateCompany, UpdateCompany
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job

settings = Settings()


@pytest.fixture
def token(company: Company) -> str:
    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "company_id": company.id}
    return JsonWebToken.encode(
        payload=payload,
        key=settings.access_token_key,
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})


async def test_retrieved_career_jobs(
    client: TestClient, headers: Headers, company: Company, job: Job
) -> None:
    response = client.get(
        url=f"/api/v1/careers/companies/{company.id}/jobs",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == job.id


async def test_retrieved_company_jobs(
    client: TestClient, headers: Headers, company: Company, job: Job
) -> None:
    response = client.get(
        url=f"/api/v1/companies/{company.id}/jobs",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == job.id


async def test_add_company_job_observers(
    client: TestClient, headers: Headers, company: Company, make_employee, job: Job
) -> None:
    created_observer = make_employee()

    response = client.put(
        url=f"/api/v1/companies/{company.id}/jobs/{job.id}/observers",
        headers=headers,
        json=json.loads(f"[{created_observer.id}]"),
    )

    assert response.status_code == 200
    assert response.json()[1]["id"] == created_observer.id


async def test_get_company_job_observers(
    client: TestClient, headers: Headers, company: Company, employee: Employee, job: Job
) -> None:
    response = client.get(
        url=f"/api/v1/companies/{company.id}/jobs/{job.id}/observers",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == employee.id


async def test_delete_company_job_observers(
    client: TestClient, headers: Headers, company: Company, employee: Employee, job: Job
) -> None:
    response = client.delete(
        url=f"/api/v1/companies/{company.id}/jobs/{job.id}/observers/{employee.id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_create_company(client: TestClient, headers: Headers) -> None:
    created_company = CreateCompany(
        name="new_company_name", overview="new_company_overview"
    )

    response = client.post(
        url="/api/v1/companies",
        headers=headers,
        json=json.loads(
            created_company.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["name"] == created_company.name
    assert response.json()["overview"] == created_company.overview


async def test_retrieve_company(
    client: TestClient, company: Company, headers: Headers
) -> None:
    response = client.get(url=f"/api/v1/companies/{company.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == company.id


async def test_retrieve_companies(
    client: TestClient, company: Company, headers: Headers
) -> None:
    response = client.get(url="/api/v1/companies", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == company.id


async def test_update_company(
    client: TestClient, company: Company, headers: Headers
) -> None:
    updated_company = UpdateCompany(
        name="updated_company_name", overview="updated_company_overview"
    )

    response = client.put(
        url=f"/api/v1/companies/{company.id}",
        headers=headers,
        json=json.loads(
            updated_company.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["id"] == company.id


async def test_delete_company(
    client: TestClient, company: Company, headers: Headers
) -> None:
    response = client.delete(url=f"/api/v1/companies/{company.id}", headers=headers)

    assert response.status_code == 200
