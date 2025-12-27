from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.talentgate.auth.exceptions import InvalidAuthorizationException
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.employee import service as employee_service
from src.talentgate.employee.exceptions import EmployeeIdNotFoundException
from src.talentgate.employee.models import (
    CreatedEmployee,
    CreateEmployee,
    DeletedEmployee,
    Employee,
    EmployeeQueryParameters,
    RetrievedEmployee,
    UpdatedEmployee,
    UpdateEmployee,
)
from src.talentgate.user.enums import UserRole
from src.talentgate.user.models import User
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["employee"])


class CreateEmployeeDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveEmployeeDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveEmployeesDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class UpdateEmployeeDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class DeleteEmployeeDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


@router.post(
    path="/api/v1/employees",
    response_model=CreatedEmployee,
    status_code=201,
    dependencies=[Depends(CreateEmployeeDependency())],
)
async def create_employee(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    employee: CreateEmployee,
) -> Employee:
    return await employee_service.create(
        sqlmodel_session=sqlmodel_session,
        company_id="company_id",
        employee=employee,
    )


@router.get(
    path="/api/v1/employees/{employee_id}",
    response_model=RetrievedEmployee,
    status_code=200,
    dependencies=[Depends(RetrieveEmployeeDependency())],
)
async def retrieve_employee(
    *,
    employee_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        employee_id=employee_id,
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    return retrieved_employee


@router.get(
    path="/api/v1/employees",
    response_model=list[RetrievedEmployee],
    status_code=200,
    dependencies=[Depends(RetrieveEmployeesDependency())],
)
async def retrieve_employees(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    query_parameters: Annotated[EmployeeQueryParameters, Query()],
) -> Sequence[Employee]:
    return await employee_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
    )


@router.put(
    path="/api/v1/employees/{employee_id}",
    response_model=UpdatedEmployee,
    status_code=200,
    dependencies=[Depends(UpdateEmployeeDependency())],
)
async def update_employee(
    *,
    employee_id: int,
    employee: UpdateEmployee,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        employee_id=employee_id,
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    return await employee_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=retrieved_employee,
        employee=employee,
    )


@router.delete(
    path="/api/v1/employees/{employee_id}",
    response_model=DeletedEmployee,
    status_code=200,
    dependencies=[Depends(DeleteEmployeeDependency())],
)
async def delete_employee(
    *,
    employee_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        employee_id=employee_id,
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    return await employee_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=retrieved_employee,
    )
