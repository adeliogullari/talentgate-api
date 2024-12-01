from typing import List, Sequence

from sqlmodel import Session
from fastapi import Depends, APIRouter
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.observer import service as observer_service
from src.talentgate.observer.exceptions import (
    IdNotFoundException,
)
from src.talentgate.job.exceptions import IdNotFoundException as JobIdNotFoundException
from src.talentgate.employee.exceptions import (
    IdNotFoundException as EmployeeIdNotFoundException,
)
from src.talentgate.observer.models import (
    Observer,
    CreateObserver,
    CreatedObserver,
    RetrievedObserver,
    UpdatedObserver,
    UpdateObserver,
    DeletedObserver,
)
from src.talentgate.job import service as job_service
from src.talentgate.employee import service as employee_service

router = APIRouter(tags=["observer"])


@router.post(
    path="/api/v1/observers",
    response_model=CreatedObserver,
    status_code=201,
)
async def create_observer(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    observer: CreateObserver,
) -> Observer:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=observer.job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=observer.employee_id
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    created_observer = await observer_service.create(
        sqlmodel_session=sqlmodel_session, observer=observer
    )

    return created_observer


@router.get(
    path="/api/v1/observers/{observer_id}",
    response_model=RetrievedObserver,
    status_code=200,
)
async def retrieve_observer(
    *, observer_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Observer:
    retrieved_observer = await observer_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, observer_id=observer_id
    )

    if not retrieved_observer:
        raise IdNotFoundException

    return retrieved_observer


@router.get(
    path="/api/v1/jobs/{job_id}/observers",
    response_model=List[RetrievedObserver],
    status_code=200,
)
async def retrieve_observers_of_single_job(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    job_id: int,
) -> Sequence[Observer]:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise IdNotFoundException

    return retrieved_job.observers


@router.put(
    path="/api/v1/observers/{observer_id}",
    response_model=UpdatedObserver,
    status_code=200,
)
async def update_observer(
    *,
    observer_id: int,
    observer: UpdateObserver,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Observer:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=observer.job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=observer.employee_id
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    retrieved_observer = await observer_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, observer_id=observer_id
    )

    if not retrieved_observer:
        raise IdNotFoundException

    updated_observer = await observer_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_observer=retrieved_observer,
        observer=observer,
    )

    return updated_observer


@router.delete(
    path="/api/v1/observers/{observer_id}",
    response_model=DeletedObserver,
    status_code=200,
)
async def delete_observer(
    *,
    observer_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Observer:
    retrieved_observer = await observer_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, observer_id=observer_id
    )

    if not retrieved_observer:
        raise IdNotFoundException

    deleted_observer = await observer_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_observer=retrieved_observer
    )

    return deleted_observer
