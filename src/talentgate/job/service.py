from typing import Any, Sequence
from sqlmodel import select, Session

from src.talentgate.job.models import (
    Job,
    CreateJob,
    UpdateJob,
    JobQueryParameters,
    JobLocation,
    CreateJobLocation,
)


async def create_job_location(
    *, sqlmodel_session: Session, job_location: CreateJobLocation
):
    created_job_location = JobLocation(
        **job_location.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_job_location)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_job_location)

    return created_job_location


async def create(*, sqlmodel_session: Session, job: CreateJob) -> Job:
    job_location = None
    if getattr(job, "location", None) is not None:
        job_location = await create_job_location(
            sqlmodel_session=sqlmodel_session, job_location=job.location
        )

    created_job = Job(
        **job.model_dump(exclude_unset=True, exclude_none=True, exclude={"location"}),
        location=job_location,
    )

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
