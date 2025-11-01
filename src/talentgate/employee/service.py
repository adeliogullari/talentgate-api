from collections.abc import Sequence
from typing import Any

from sqlmodel import Session, select

from src.talentgate.employee.models import (
    CreateEmployee,
    Employee,
    EmployeeQueryParameters,
    UpdateEmployee,
    UpsertEmployee,
)
from src.talentgate.user import service as user_service
from src.talentgate.user.models import User


async def create(*, sqlmodel_session: Session, employee: CreateEmployee) -> Employee:
    created_employee = Employee(
        **employee.model_dump(exclude_unset=True, exclude_none=True, exclude={"user"}),
    )

    if getattr(employee, "user", None):
        created_employee.user = await user_service.upsert(
            sqlmodel_session=sqlmodel_session,
            user=employee.user,
        )

    sqlmodel_session.add(created_employee)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_employee)

    return created_employee


async def retrieve_by_id(*, sqlmodel_session: Session, employee_id: int) -> Employee:
    statement: Any = select(Employee).where(Employee.id == employee_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_query_parameters(
    *,
    sqlmodel_session: Session,
    query_parameters: EmployeeQueryParameters,
) -> Sequence[Employee]:
    offset = query_parameters.offset
    limit = query_parameters.limit

    employee_filters = [
        getattr(Employee, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit", "user"},
            exclude_unset=True,
            exclude_none=True,
        ).items()
    ]

    user_filters = []
    if getattr(query_parameters, "user", None):
        user_filters = [
            getattr(User, attr) == value
            for attr, value in query_parameters.user.model_dump(
                exclude={"offset", "limit", "user"},
                exclude_unset=True,
                exclude_none=True,
            ).items()
        ]

    filters = employee_filters + user_filters

    statement: Any = (
        select(Employee).join(User).offset(offset).limit(limit).where(*filters)
    )

    return sqlmodel_session.exec(statement).all()


async def update(
    *,
    sqlmodel_session: Session,
    retrieved_employee: Employee,
    employee: UpdateEmployee,
) -> Employee:
    if getattr(employee, "user", None) is not None:
        await user_service.upsert(sqlmodel_session=sqlmodel_session, user=employee.user)

    retrieved_employee.sqlmodel_update(
        employee.model_dump(exclude_none=True, exclude_unset=True, exclude={"user"}),
    )

    sqlmodel_session.add(retrieved_employee)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_employee)

    return retrieved_employee


async def upsert(
    *,
    sqlmodel_session: Session,
    employee: UpsertEmployee,
) -> Employee:
    retrieved_employee = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        employee_id=employee.id,
    )
    if retrieved_employee:
        return await update(
            sqlmodel_session=sqlmodel_session,
            retrieved_employee=retrieved_employee,
            employee=UpdateEmployee(
                **employee.model_dump(
                    exclude_none=True, exclude_unset=True, exclude={"id"}
                )
            ),
        )
    return await create(
        sqlmodel_session=sqlmodel_session,
        employee=CreateEmployee(
            **employee.model_dump(exclude_none=True, exclude_unset=True, exclude={"id"})
        ),
    )


async def delete(
    *,
    sqlmodel_session: Session,
    retrieved_employee: Employee,
) -> Employee:
    sqlmodel_session.delete(retrieved_employee)
    sqlmodel_session.commit()

    return retrieved_employee
