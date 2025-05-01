from sqlmodel import Session
from src.talentgate.employee.enums import EmployeeTitle
from src.talentgate.employee.models import (
    CreateEmployee,
    Employee,
    UpdateEmployee,
)
from src.talentgate.employee import service as employee_service
from src.talentgate.employee.service import create, delete, retrieve_by_id, update
from src.talentgate.user.enums import UserRole
from src.talentgate.user.models import CreateUser, UpdateUser


async def test_create(sqlmodel_session: Session) -> None:
    user = CreateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ADMIN,
    )

    employee = CreateEmployee(title=EmployeeTitle.FOUNDER, user=user)

    created_employee = await create(
        sqlmodel_session=sqlmodel_session,
        employee=employee,
    )

    assert created_employee.title == employee.title


async def test_retrieve_by_id(sqlmodel_session: Session, employee: Employee) -> None:
    retrieved_employee = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        employee_id=employee.id,
    )

    assert retrieved_employee.id == employee.id


async def test_update(sqlmodel_session: Session, make_employee) -> None:
    retrieved_employee = make_employee()

    user = UpdateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ADMIN,
    )

    employee = UpdateEmployee(title=EmployeeTitle.FOUNDER, user=user)

    updated_employee = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=retrieved_employee,
        employee=employee,
    )

    assert employee.title == updated_employee.title


async def test_upsert_create(sqlmodel_session: Session) -> None:
    user = CreateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ADMIN,
    )

    employee = CreateEmployee(title=EmployeeTitle.FOUNDER, user=user)

    created_employee = await employee_service.upsert(
        sqlmodel_session=sqlmodel_session,
        employee=employee,
    )

    assert created_employee.title == employee.title


async def test_upsert_update(sqlmodel_session: Session, make_employee) -> None:
    retrieved_employee = make_employee()

    user = UpdateUser(
        id=retrieved_employee.user_id,
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ADMIN,
    )

    employee = CreateEmployee(
        id=retrieved_employee.id, title=EmployeeTitle.FOUNDER, user=user
    )

    updated_employee = await employee_service.upsert(
        sqlmodel_session=sqlmodel_session,
        employee=employee,
    )

    assert updated_employee.id == employee.id
    assert updated_employee.user.id == user.id


async def test_delete(sqlmodel_session: Session, employee: Employee) -> None:
    deleted_employee = await delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=employee,
    )

    assert deleted_employee.title == employee.title
