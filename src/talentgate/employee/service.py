from typing import Any, Sequence
from sqlmodel import select, Session
from src.talentgate.employee.models import Employee, CreateEmployee, UpdateEmployee


async def create(*, sqlmodel_session: Session, employee: CreateEmployee) -> Employee:
    created_employee = Employee(
        **employee.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_employee)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_employee)

    return created_employee


async def retrieve_by_id(*, sqlmodel_session: Session, employee_id: int) -> Employee:
    statement: Any = select(Employee).where(Employee.id == employee_id)

    retrieved_employee = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_employee


async def update(
    *, sqlmodel_session: Session, retrieved_employee: Employee, employee: UpdateEmployee
) -> Employee:
    retrieved_employee.sqlmodel_update(employee)

    sqlmodel_session.add(retrieved_employee)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_employee)

    return retrieved_employee


async def delete(
    *, sqlmodel_session: Session, retrieved_employee: Employee
) -> Employee:
    sqlmodel_session.delete(retrieved_employee)
    sqlmodel_session.commit()

    return retrieved_employee
