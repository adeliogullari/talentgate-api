import json
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from pytography import JsonWebToken
from starlette.datastructures import Headers

from config import Settings
from src.talentgate.application.models import (
    Application,
    ApplicationEvaluation,
    ApplicationEvaluationRequest,
    CreateApplication,
    CreateResume,
    UpdateApplication,
)

settings = Settings()


async def test_create_application(client: TestClient, headers: Headers) -> None:
    created_application = CreateApplication(
        firstname="created firstname",
        lastname="created lastname",
        email="created_applicant_email@gmail.com",
        phone="+90532556345",
        resume=CreateResume(name="resume", data=b"data"),
    )

    response = client.post(
        url="/api/v1/applications",
        headers=headers,
        json=json.loads(
            created_application.model_dump_json(exclude_none=True, exclude_unset=True),
        ),
    )

    assert response.status_code == 201
    assert response.json()["email"] == created_application.email


async def test_retrieve_application(
    client: TestClient,
    application: Application,
    resume,
    headers: Headers,
) -> None:
    response = client.get(url=f"/api/v1/applications/{application.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == application.id
    assert response.json()["email"] == application.email


async def test_retrieve_applications(
    client: TestClient,
    application: Application,
    resume,
    headers: Headers,
) -> None:
    response = client.get(url="/api/v1/applications", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == application.id


async def test_update_application(
    client: TestClient,
    application: Application,
    headers: Headers,
) -> None:
    updated_application = UpdateApplication(
        firstname="updated firstname",
        lastname="updated lastname",
        email="updated_email@gmail.com",
        phone="+90532556999",
        resume="updated_resume.pdf",
    )

    response = client.put(
        url=f"/api/v1/applications/{application.id}",
        headers=headers,
        json=json.loads(
            updated_application.model_dump_json(exclude_none=True, exclude_unset=True),
        ),
    )

    assert response.status_code == 200
    assert response.json()["email"] == updated_application.email


async def test_delete_application(
    client: TestClient,
    application: Application,
    headers: Headers,
) -> None:
    response = client.delete(
        url=f"/api/v1/applications/{application.id}",
        headers=headers,
    )

    assert response.status_code == 200
