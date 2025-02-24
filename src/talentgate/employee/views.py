from typing import List, Sequence

from sqlmodel import Session
from fastapi import Depends, APIRouter, Query
from src.talentgate.user.views import retrieve_current_user
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.employee import service as employee_service
from src.talentgate.employee.exceptions import EmployeeIdNotFoundException
from src.talentgate.user.models import UserRole, User
from src.talentgate.employee.models import (
    Employee,
    CreateEmployee,
    CreatedEmployee,
    RetrievedEmployee,
    EmployeeQueryParameters,
    UpdatedEmployee,
    UpdateEmployee,
    DeletedEmployee,
)
from src.talentgate.auth.exceptions import (
    InvalidAuthorizationException,
)

router = APIRouter(tags=["employee"])


class CreateEmployeeDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveEmployeeDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveEmployeesDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class UpdateEmployeeDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class DeleteEmployeeDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
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
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    employee: CreateEmployee,
) -> Employee:
    created_employee = await employee_service.create(
        sqlmodel_session=sqlmodel_session, employee=employee
    )

    return created_employee


@router.get(
    path="/api/v1/employees/{employee_id}",
    response_model=RetrievedEmployee,
    status_code=200,
    dependencies=[Depends(RetrieveEmployeeDependency())],
)
async def retrieve_employee(
    *, employee_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=employee_id
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    return retrieved_employee


@router.get(
    path="/api/v1/employees",
    response_model=List[RetrievedEmployee],
    status_code=200,
    dependencies=[Depends(RetrieveEmployeesDependency())],
)
async def retrieve_employees(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: EmployeeQueryParameters = Query(),
) -> Sequence[Employee]:
    retrieved_employee = await employee_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_employee


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
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=employee_id
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    updated_employee = await employee_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=retrieved_employee,
        employee=employee,
    )

    return updated_employee


@router.delete(
    path="/api/v1/employees/{employee_id}",
    response_model=DeletedEmployee,
    status_code=200,
    dependencies=[Depends(DeleteEmployeeDependency())],
)
async def delete_employee(
    *,
    employee_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=employee_id
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    deleted_employee = await employee_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_employee=retrieved_employee
    )

    return deleted_employee
