import json

import pytest
from fastapi.testclient import TestClient
from starlette.datastructures import Headers

from config import get_settings
from src.talentgate.employee.enums import EmployeeTitle
from src.talentgate.employee.models import (
    CreateEmployee,
    Employee,
    UpdateEmployee,
)
from src.talentgate.user.models import UserRole, CreateUser

settings = get_settings()


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_create_employee(client: TestClient, headers: Headers) -> None:
    user = CreateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ADMIN,
    )

    created_employee = CreateEmployee(title=EmployeeTitle.FOUNDER, user=user)

    response = client.post(
        url="/api/v1/employees",
        headers=headers,
        json=json.loads(
            created_employee.model_dump_json(exclude_none=True, exclude_unset=True),
        ),
    )

    assert response.status_code == 201
    assert response.json()["title"] == created_employee.title
    assert response.json()["email"] == user.email


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_employee(
    client: TestClient,
    employee: Employee,
    headers: Headers,
) -> None:
    response = client.get(url=f"/api/v1/employees/{employee.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == employee.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_employees(
    client: TestClient,
    employee: Employee,
    headers: Headers,
) -> None:
    params = {
        "id": employee.id,
        "title": employee.title,
        "user.id": employee.user.id,
        "user.firstname": employee.user.firstname,
        "user.lastname": employee.user.lastname,
        "user.username": employee.user.username,
        "user.email": employee.user.email,
        "user.verified": employee.user.verified,
        "user.role": employee.user.role,
    }

    response = client.get(url="/api/v1/employees", params=params, headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == employee.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_update_employee(
    client: TestClient,
    employee: Employee,
    headers: Headers,
) -> None:
    updated_employee = UpdateEmployee(title=EmployeeTitle.FOUNDER)

    response = client.put(
        url=f"/api/v1/employees/{employee.id}",
        headers=headers,
        json=json.loads(
            updated_employee.model_dump_json(exclude_none=True, exclude_unset=True),
        ),
    )

    assert response.status_code == 200
    assert response.json()["id"] == employee.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_delete_employee(
    client: TestClient,
    employee: Employee,
    headers: Headers,
) -> None:
    response = client.delete(url=f"/api/v1/employees/{employee.id}", headers=headers)

    assert response.status_code == 200
