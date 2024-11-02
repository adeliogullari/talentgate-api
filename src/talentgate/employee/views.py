from typing import List, Sequence

from sqlmodel import Session
from fastapi import Depends, APIRouter, Query
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.employee import service as employee_service
from src.talentgate.employee.models import (
    Employee,
    CreateEmployee,
    CreatedEmployee,
    RetrievedEmployee,
    UpdateEmployee,
    UpdatedEmployee,
    DeletedEmployee,
)
from src.talentgate.user.models import DeletedUser

router = APIRouter(tags=["employee"])


@router.post(
    path="/api/v1/employees",
    response_model=CreatedEmployee,
    status_code=201,
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
)
async def retrieve_employee(
    *, employee_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=employee_id
    )

    return retrieved_employee
