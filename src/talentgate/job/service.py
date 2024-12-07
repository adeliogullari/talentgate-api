from typing import Any, Sequence, List
from sqlmodel import select, Session

from src.talentgate.employee.models import Employee
from src.talentgate.job.models import (
    Job,
    CreateJob,
    UpdateJob,
    JobQueryParameters,
    AddedObserver,
    RetrievedObserver,
    DeletedObserver,
)
from src.talentgate.link.models import Observer


# Observer Service
async def add_observers(
    *, sqlmodel_session: Session, job: Job, employees: List[Employee]
) -> Sequence[AddedObserver]:
    added_observers: List[AddedObserver] = []
    for employee in employees:
        job.observers.append(employee)
        added_observers.append(AddedObserver(job_id=job.id, employee_id=employee.id))

    sqlmodel_session.commit()
    sqlmodel_session.refresh(job)

    return added_observers


async def retrieve_observer_by_job_and_employee(
    *, sqlmodel_session: Session, job: Job, employee: Employee
) -> RetrievedObserver:
    statement: Any = select(Observer).where(
        (Observer.job_id == job.id) and (Observer.employee_id == employee.id)
    )
    retrieved_observer = sqlmodel_session.exec(statement).one_or_none()

    if retrieved_observer is not None:
        return RetrievedObserver(job_id=job.id, employee_id=employee.id)


async def retrieve_observers_of_single_job(*, job: Job) -> Sequence[RetrievedObserver]:
    retrieved_observers = job.observers

    formatted_observers = []
    for observer in retrieved_observers:
        formatted_observer = RetrievedObserver(job_id=job.id, employee_id=observer.id)

        formatted_observers.append(formatted_observer)

    return formatted_observers


async def delete_observer(
    *, sqlmodel_session: Session, job: Job, employee: Employee
) -> DeletedObserver:
    job.observers.remove(employee)

    sqlmodel_session.commit()
    sqlmodel_session.refresh(job)

    return DeletedObserver(job_id=job.id, employee_id=employee.id)


# Job Service
async def create(*, sqlmodel_session: Session, job: CreateJob) -> Job:
    created_job = Job(**job.model_dump(exclude_unset=True, exclude_none=True))

    sqlmodel_session.add(created_job)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_job)

    return created_job


async def retrieve_by_id(*, sqlmodel_session: Session, job_id: int) -> Job:
    statement: Any = select(Job).where(Job.id == job_id)

    retrieved_job = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_job


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: JobQueryParameters
) -> Sequence[Job]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Job, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        )
    }

    statement: Any = select(Job).offset(offset).limit(limit).where(*filters)

    retrieved_job = sqlmodel_session.exec(statement).all()

    return retrieved_job


async def update(
    *, sqlmodel_session: Session, retrieved_job: Job, job: UpdateJob
) -> Job:
    retrieved_job.sqlmodel_update(job)

    sqlmodel_session.add(retrieved_job)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_job)

    return retrieved_job


async def delete(*, sqlmodel_session: Session, retrieved_job: Job) -> Job:
    sqlmodel_session.delete(retrieved_job)
    sqlmodel_session.commit()

    return retrieved_job
