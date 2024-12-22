from sqlmodel import Session
from src.talentgate.employee.models import (
    Employee,
    CreateEmployee,
    EmployeeTitle,
    UpdateEmployee,
)
from src.talentgate.employee.service import create, retrieve_by_id, update, delete


async def test_create(sqlmodel_session: Session) -> None:
    new_employee = CreateEmployee(
        title=EmployeeTitle.FOUNDER,
    )

    created_employee = await create(
        sqlmodel_session=sqlmodel_session, employee=new_employee
    )

    assert created_employee.title == new_employee.title


async def test_retrieve_by_id(sqlmodel_session: Session, employee: Employee) -> None:
    retrieved_employee = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=employee.id
    )

    assert retrieved_employee.id == employee.id


async def test_update(sqlmodel_session: Session, employee: Employee) -> None:
    modified_employee = UpdateEmployee(
        title=EmployeeTitle.FOUNDER,
    )

    updated_employee = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=employee,
        employee=modified_employee,
    )

    assert employee.title == updated_employee.title


async def test_delete(sqlmodel_session: Session, employee: Employee) -> None:
    deleted_employee = await delete(
        sqlmodel_session=sqlmodel_session, retrieved_employee=employee
    )

    assert deleted_employee.title == employee.title
