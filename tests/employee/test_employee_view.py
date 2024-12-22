import json
import pytest
from datetime import timedelta, datetime, UTC
from config import Settings
from src.talentgate.employee.models import (
    Employee,
    CreateEmployee,
    EmployeeTitle,
    UpdateEmployee,
)
from pytography import JsonWebToken
from starlette.datastructures import Headers
from fastapi.testclient import TestClient

settings = Settings()


async def test_create_employee(client: TestClient, headers: Headers) -> None:
    created_employee = CreateEmployee(title=EmployeeTitle.FOUNDER)

    response = client.post(
        url="/api/v1/employees",
        headers=headers,
        json=json.loads(
            created_employee.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 201
    assert response.json()["title"] == created_employee.title


async def test_retrieve_employee(
    client: TestClient, employee: Employee, headers: Headers
) -> None:
    response = client.get(url=f"/api/v1/employees/{employee.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == employee.id


async def test_retrieve_employees(
    client: TestClient, employee: Employee, headers: Headers
) -> None:
    response = client.get(url="/api/v1/employees", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == employee.id


async def test_update_employee(
    client: TestClient, employee: Employee, headers: Headers
) -> None:
    updated_employee = UpdateEmployee(title=EmployeeTitle.FOUNDER)

    response = client.put(
        url=f"/api/v1/employees/{employee.id}",
        headers=headers,
        json=json.loads(
            updated_employee.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["id"] == employee.id


async def test_delete_employee(
    client: TestClient, employee: Employee, headers: Headers
) -> None:
    response = client.delete(url=f"/api/v1/employees/{employee.id}", headers=headers)

    assert response.status_code == 200
