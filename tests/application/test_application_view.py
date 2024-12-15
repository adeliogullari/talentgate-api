import json

import pytest
from datetime import timedelta, datetime, UTC


from config import Settings
from src.talentgate.application.models import (
    Application,
    ApplicationEvaluation,
    ApplicationEvaluationRequest,
    ApplicationRequest,
)
from pytography import JsonWebToken
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

settings = Settings()


@pytest.fixture
def token(application: Application) -> str:
    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "application_id": application.id}
    return JsonWebToken.encode(
        payload=payload,
        key=settings.access_token_key,
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})


async def test_create_application_evaluation(
    client: TestClient, application: Application, headers
) -> None:
    created_evaluation = ApplicationEvaluationRequest(comment="new_comment", rating="5")

    response = client.post(
        url="/api/v1/applications/evaluations",
        headers=headers,
        json=json.loads(
            created_evaluation.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["comment"] == created_evaluation.comment


async def test_retrieve_application_evaluation(
    client: TestClient, application_evaluation: ApplicationEvaluation, headers
) -> None:
    response = client.get(
        url=f"/api/v1/applications/evaluations/{application_evaluation.id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == application_evaluation.id
    assert response.json()["comment"] == application_evaluation.comment


async def test_retrieve_application_evaluations_by_application(
    client: TestClient, application_evaluation: ApplicationEvaluation, headers
) -> None:
    response = client.get(
        url=f"/api/v1/applications/{application_evaluation.application_id}/evaluations",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["application_id"] == application_evaluation.application_id
    assert response.json()[0]["id"] == application_evaluation.id
    assert response.json()[0]["comment"] == application_evaluation.comment


async def test_update_application_evaluation(
    client: TestClient, application_evaluation: ApplicationEvaluation, headers
) -> None:
    updated_application_evaluation = ApplicationEvaluationRequest(
        comment="updated_comment", rating="4"
    )

    response = client.put(
        url=f"/api/v1/applications/evaluations/{application_evaluation.id}",
        headers=headers,
        json=json.loads(
            updated_application_evaluation.model_dump_json(
                exclude_none=True, exclude_unset=True
            )
        ),
    )

    assert response.status_code == 200
    assert response.json()["comment"] == updated_application_evaluation.comment


async def test_delete_application_evaluation(
    client: TestClient, application_evaluation: ApplicationEvaluation, headers
) -> None:
    response = client.delete(
        url=f"/api/v1/applications/evaluations/{application_evaluation.id}",
        headers=headers,
    )

    assert response.status_code == 200


async def test_create_application(client: TestClient, headers: Headers) -> None:
    created_application = ApplicationRequest(
        firstname="created firstname",
        lastname="created lastname",
        email="created_applicant_email@gmail.com",
        phone="+90532556345",
        resume="created_resume.pdf",
    )

    response = client.post(
        url="/api/v1/applications",
        headers=headers,
        json=json.loads(
            created_application.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["email"] == created_application.email


async def test_retrieve_application(
    client: TestClient, application: Application, headers: Headers
) -> None:
    response = client.get(url=f"/api/v1/applications/{application.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == application.id
    assert response.json()["email"] == application.email


async def test_retrieve_applications(
    client: TestClient, application: Application, headers: Headers
) -> None:
    response = client.get(url="/api/v1/applications", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == application.id


async def test_update_application(
    client: TestClient, application: Application, headers: Headers
) -> None:
    updated_application = ApplicationRequest(
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
            updated_application.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["email"] == updated_application.email


async def test_delete_application(
    client: TestClient, application: Application, headers: Headers
) -> None:
    response = client.delete(
        url=f"/api/v1/applications/{application.id}", headers=headers
    )

    assert response.status_code == 200
