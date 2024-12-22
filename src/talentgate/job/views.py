from typing import List, Sequence

from sqlmodel import Session
from fastapi import Depends, APIRouter, Query, HTTPException
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.employee.models import Employee
from src.talentgate.job import service as job_service
from src.talentgate.employee import service as employee_service
from src.talentgate.job.exceptions import (
    IdNotFoundException as JobIdNotFoundException,
    ObserverAlreadyExistsException,
    ObserverNotFoundException,
)
from src.talentgate.employee.exceptions import (
    IdNotFoundException as EmployeeIdNotFoundException,
)
from src.talentgate.job.models import (
    Job,
    CreateJob,
    CreatedJob,
    RetrievedJob,
    JobQueryParameters,
    UpdatedJob,
    UpdateJob,
    DeletedJob,
    AddObserver,
    AddedObserver,
    RetrievedObserver,
    DeletedObserver,
)
from src.talentgate.database.models import Observer

router = APIRouter(tags=["job"])


# Observer Endpoints
@router.post(
    path="/api/v1/jobs/{job_id}/observers",
    response_model=List[AddedObserver],
    status_code=201,
)
async def create_observer(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    job_id: int,
    observers: List[AddObserver],
) -> Sequence[Observer]:
    # Retrieve job with job_id and verify it exists
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    # Retrieve employees with employee_id's and verify they exist
    retrieved_employees: List[Employee] = []
    for observer in observers:
        retrieved_employee = await employee_service.retrieve_by_id(
            sqlmodel_session=sqlmodel_session, employee_id=observer.employee_id
        )

        if not retrieved_employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with id {observer.employee_id} not found",
            )

        # Check if observer already exists
        retrieved_observer_by_job_and_employee = (
            await job_service.retrieve_observer_by_job_and_employee(
                sqlmodel_session=sqlmodel_session,
                job=retrieved_job,
                employee=retrieved_employee,
            )
        )

        if retrieved_observer_by_job_and_employee:
            raise ObserverAlreadyExistsException

        retrieved_employees.append(retrieved_employee)

    # Add observers to job
    added_observer = await job_service.add_observers(
        sqlmodel_session=sqlmodel_session,
        job=retrieved_job,
        employees=retrieved_employees,
    )

    return added_observer


@router.get(
    path="/api/v1/jobs/{job_id}/observers",
    response_model=List[RetrievedObserver],
    status_code=200,
)
async def retrieve_observers(
    *, job_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Sequence[Observer]:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    retrieved_observers = await job_service.retrieve_observers_of_single_job(
        job=retrieved_job
    )

    return retrieved_observers


@router.delete(
    path="/api/v1/jobs/{job_id}/observers/{employee_id}",
    response_model=DeletedObserver,
    status_code=200,
)
async def delete_observer(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    job_id: int,
    employee_id: int,
) -> Observer:
    # Retrieve job and check if it exists
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    # Retrieve employee and check if it exists
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=employee_id
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    # Check if observer exists
    retrieved_observer_by_job_and_employee = (
        await job_service.retrieve_observer_by_job_and_employee(
            sqlmodel_session=sqlmodel_session,
            job=retrieved_job,
            employee=retrieved_employee,
        )
    )

    if not retrieved_observer_by_job_and_employee:
        raise ObserverNotFoundException

    # Delete observer
    deleted_observer = await job_service.delete_observer(
        sqlmodel_session=sqlmodel_session,
        job=retrieved_job,
        employee=retrieved_employee,
    )

    return deleted_observer


# Job Endpoints
@router.post(
    path="/api/v1/jobs",
    response_model=CreatedJob,
    status_code=201,
)
async def create_job(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    job: CreateJob,
) -> Job:
    created_job = await job_service.create(sqlmodel_session=sqlmodel_session, job=job)

    return created_job


@router.get(
    path="/api/v1/jobs/{job_id}",
    response_model=RetrievedJob,
    status_code=200,
)
async def retrieve_job(
    *, job_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    return retrieved_job


@router.get(
    path="/api/v1/jobs",
    response_model=List[RetrievedJob],
    status_code=200,
)
async def retrieve_jobs(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: JobQueryParameters = Query(),
) -> Sequence[Job]:
    retrieved_job = await job_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_job


@router.put(path="/api/v1/jobs/{job_id}", response_model=UpdatedJob, status_code=200)
async def update_job(
    *,
    job_id: int,
    job: UpdateJob,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    updated_job = await job_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_job=retrieved_job, job=job
    )

    return updated_job


@router.delete(path="/api/v1/jobs/{job_id}", response_model=DeletedJob, status_code=200)
async def delete_job(
    *,
    job_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    deleted_job = await job_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_job=retrieved_job
    )

    return deleted_job
