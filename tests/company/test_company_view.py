import json
from datetime import UTC, datetime, timedelta
from io import BytesIO
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from minio import Minio
from starlette.datastructures import Headers

from config import get_settings
from src.talentgate.company.enums import CompanyEmployeeTitle
from src.talentgate.company.models import Company, CreateCompany, UpdateCompany
from src.talentgate.job.models import Job
from src.talentgate.user.models import UserSubscriptionPlan, UserRole, User

settings = get_settings()


async def test_retrieved_career_jobs(
    client: TestClient,
    headers: Headers,
    company: Company,
    job: Job,
) -> None:
    response = client.get(
        url=f"/api/v1/careers/companies/{company.id}/jobs",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == job.id


async def test_retrieved_career_job(
    client: TestClient,
    headers: Headers,
    company: Company,
    job: Job,
) -> None:
    response = client.get(
        url=f"/api/v1/careers/companies/{company.id}/jobs/{job.id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == job.id


async def test_retrieved_company_jobs(
    client: TestClient,
    headers: Headers,
    company: Company,
    job: Job,
) -> None:
    response = client.get(
        url=f"/api/v1/companies/{company.id}/jobs",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == job.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_create_company(client: TestClient, headers: Headers) -> None:
    created_company = CreateCompany(
        name="new_company_name",
        overview="new_company_overview",
    )

    response = client.post(
        url="/api/v1/companies",
        headers=headers,
        json=json.loads(
            created_company.model_dump_json(exclude_none=True, exclude_unset=True),
        ),
    )

    assert response.status_code == 201
    assert response.json()["name"] == created_company.name
    assert response.json()["overview"] == created_company.overview


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_company(
    client: TestClient,
    company: Company,
    headers: Headers,
) -> None:
    response = client.get(url=f"/api/v1/companies/{company.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == company.id


@pytest.mark.parametrize("company_employee", [{"title": CompanyEmployeeTitle.FOUNDER}], indirect=True)
async def test_retrieve_current_company(client: TestClient, company: Company, headers: Headers) -> None:
    response = client.get(url="/api/v1/me/company", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == company.id


async def test_retrieve_current_company_logo(
    client: TestClient, minio_client: Minio, company: Company, headers: Headers
) -> None:
    data = b"data"

    minio_client.put_object(
        bucket_name="talentgate",
        object_name=f"companies/{company.id}/logo",
        data=BytesIO(data),
        length=4,
        content_type="file",
    )

    response = client.get(url="/api/v1/me/company/logo", headers=headers)

    assert response.status_code == 200
    assert response.content == data


async def test_upload_current_company_logo(
    client: TestClient, minio_client: Minio, company: Company, headers: Headers
) -> None:
    data = b"data"
    file_stream = BytesIO(data)

    response = client.post(
        url="/api/v1/me/company/logo",
        files={"file": ("logo.jpg", file_stream, "octet/stream")},
        headers=headers,
    )

    logo = minio_client.get_object(bucket_name="talentgate", object_name=f"companies/{company.id}/logo")

    assert response.status_code == 201
    assert logo.data == data


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_companies(
    client: TestClient,
    company: Company,
    headers: Headers,
) -> None:
    response = client.get(url="/api/v1/companies", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == company.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_update_company(
    client: TestClient,
    company: Company,
    headers: Headers,
) -> None:
    updated_company = UpdateCompany(
        name="updated_company_name",
        overview="updated_company_overview",
    )

    response = client.put(
        url=f"/api/v1/companies/{company.id}",
        headers=headers,
        json=json.loads(
            updated_company.model_dump_json(exclude_none=True, exclude_unset=True),
        ),
    )

    assert response.status_code == 200
    assert response.json()["id"] == company.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_delete_company(
    client: TestClient,
    company: Company,
    headers: Headers,
) -> None:
    response = client.delete(url=f"/api/v1/companies/{company.id}", headers=headers)

    assert response.status_code == 200
