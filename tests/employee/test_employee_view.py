import json
import pytest
from datetime import timedelta, datetime, UTC
from config import Settings
from src.talentgate.auth.crypto.token import BearerToken
from src.talentgate.employee.models import (
    Employee,
    CreateEmployee,
    EmployeeTitle,
    UpdateEmployee,
)
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

settings = Settings()


@pytest.fixture
def token(employee: Employee) -> str:
    access_token = BearerToken("blake2b")

    now = datetime.now(UTC)
    exp = (now + timedelta(minutes=60)).timestamp()
    payload = {"exp": exp, "employee_id": employee.id}
    return access_token.encode(
        payload=payload,
        key=settings.access_token_key,
        headers={"alg": settings.access_token_algorithm, "typ": "JWT"},
    )


@pytest.fixture
def headers(token: str) -> Headers:
    return Headers({"Authorization": f"Bearer {token}"})


async def test_create_employee(client: TestClient, headers: Headers) -> None:
    created_employee = CreateEmployee(title=EmployeeTitle.FOUNDER, salary="999")

    response = client.post(
        url=f"/api/v1/employees",
        headers=headers,
        json=json.loads(
            created_employee.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["title"] == created_employee.title
    assert response.json()["salary"] == created_employee.salary


async def test_retrieve_employee(
    client: TestClient, employee: Employee, headers: Headers
) -> None:
    response = client.get(url=f"/api/v1/employees/{employee.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == employee.id
    assert response.json()["title"] == employee.title
    assert response.json()["salary"] == employee.salary


async def test_retrieve_employees(
    client: TestClient, employee: Employee, headers: Headers
) -> None:
    response = client.get(url="/api/v1/employees", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == employee.id
    assert response.json()[0]["title"] == employee.title
    assert response.json()[0]["salary"] == employee.salary


async def test_update_employee(
    client: TestClient, employee: Employee, headers: Headers
) -> None:
    updated_employee = UpdateEmployee(title=EmployeeTitle.FOUNDER, salary="987")

    response = client.put(
        url=f"/api/v1/employees/{employee.id}",
        headers=headers,
        json=json.loads(
            updated_employee.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["id"] == employee.id
    assert response.json()["title"] == employee.title
    assert response.json()["salary"] == employee.salary


async def test_delete_employee(
    client: TestClient, employee: Employee, headers: Headers
) -> None:
    response = client.delete(url=f"/api/v1/employees/{employee.id}", headers=headers)

    assert response.status_code == 200
