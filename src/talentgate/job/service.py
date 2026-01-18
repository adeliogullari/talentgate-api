from collections.abc import Sequence
from typing import Any

from sqlmodel import Session, select

from src.talentgate.job.models import (
    CreateJob,
    CreateJobLocation,
    CreateJobLocationAddress,
    CreateSalary,
    Job,
    JobLocation,
    JobLocationAddress,
    JobQueryParameters,
    JobSalary,
    UpdateJob,
    UpdateJobLocation,
    UpdateJobLocationAddress,
    UpdateSalary,
)


async def create_location_address(
    *,
    sqlmodel_session: Session,
    location_id: int,
    address: CreateJobLocationAddress,
) -> JobLocationAddress:
    created_address = JobLocationAddress(
        **address.model_dump(exclude_unset=True, exclude_none=True),
        location_id=location_id,
    )

    sqlmodel_session.add(created_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_address)

    return created_address


async def retrieve_location_address_by_id(
    *,
    sqlmodel_session: Session,
    location_id: int,
    address_id: int,
) -> JobLocationAddress:
    statement: Any = select(JobLocationAddress).where(
        JobLocationAddress.location_id == location_id, JobLocationAddress.id == address_id
    )

    return sqlmodel_session.exec(statement).one_or_none()


async def update_location_address(
    *,
    sqlmodel_session: Session,
    retrieved_address: JobLocationAddress,
    address: UpdateJobLocationAddress,
) -> JobLocationAddress:
    retrieved_address.sqlmodel_update(
        address.model_dump(exclude_none=True, exclude_unset=True),
    )

    sqlmodel_session.add(retrieved_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_address)

    return retrieved_address


async def create_location(
    *,
    sqlmodel_session: Session,
    job_id: int,
    location: CreateJobLocation,
) -> JobLocation:
    created_location = JobLocation(
        **location.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"address"},
        ),
        job_id=job_id,
    )

    if "address" in location.model_fields_set and location.address is not None:
        created_location.address = await create_location_address(
            sqlmodel_session=sqlmodel_session, location_id=created_location.id, address=location.address
        )

    sqlmodel_session.add(created_location)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_location)

    return created_location


async def retrieve_location_by_id(
    *,
    sqlmodel_session: Session,
    job_id: int,
    location_id: int,
) -> JobLocation:
    statement: Any = select(JobLocation).where(JobLocation.job_id == job_id, JobLocation.id == location_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def update_location(
    *,
    sqlmodel_session: Session,
    retrieved_location: JobLocation,
    location: UpdateJobLocation,
) -> JobLocation:
    if "address" in location.model_fields_set and location.address is not None:
        retrieved_address = await retrieve_location_address_by_id(
            sqlmodel_session=sqlmodel_session,
            location_id=retrieved_location.id,
            address_id=retrieved_location.address.id,
        )

        retrieved_location.address = await update_location_address(
            sqlmodel_session=sqlmodel_session,
            retrieved_address=retrieved_address,
            address=location.address,
        )

    retrieved_location.sqlmodel_update(
        location.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude={"address"},
        ),
    )

    sqlmodel_session.add(retrieved_location)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_location)

    return retrieved_location


async def create_salary(
    *,
    sqlmodel_session: Session,
    job_id: int,
    salary: CreateSalary,
) -> JobSalary:
    created_salary = JobSalary(**salary.model_dump(exclude_unset=True, exclude_none=True), job_id=job_id)

    sqlmodel_session.add(created_salary)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_salary)

    return created_salary


async def retrieve_salary_by_id(
    *,
    sqlmodel_session: Session,
    job_id: int,
    salary_id: int,
) -> JobSalary:
    statement: Any = select(JobSalary).where(JobSalary.job_id == job_id, JobSalary.id == salary_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def update_salary(
    *,
    sqlmodel_session: Session,
    retrieved_salary: JobSalary,
    salary: UpdateSalary,
) -> JobSalary:
    retrieved_salary.sqlmodel_update(
        salary.model_dump(exclude_none=True, exclude_unset=True),
    )

    sqlmodel_session.add(retrieved_salary)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_salary)

    return retrieved_salary


async def create(*, sqlmodel_session: Session, job: CreateJob) -> Job:
    created_job = Job(
        **job.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"location", "salary"},
        ),
    )

    if "location" in job.model_fields_set and job.location is not None:
        created_job.location = await create_location(
            sqlmodel_session=sqlmodel_session, job_id=created_job.id, location=job.location
        )

    if "salary" in job.model_fields_set and job.location is not None:
        created_job.salary = await create_salary(
            sqlmodel_session=sqlmodel_session, job_id=created_job.id, salary=job.salary
        )

    sqlmodel_session.add(created_job)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_job)

    return created_job


async def retrieve_by_id(*, sqlmodel_session: Session, job_id: int) -> Job:
    statement: Any = select(Job).where(Job.id == job_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_query_parameters(
    *,
    sqlmodel_session: Session,
    query_parameters: JobQueryParameters,
) -> Sequence[Job]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Job, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"},
            exclude_unset=True,
            exclude_none=True,
        )
    }

    statement: Any = select(Job).offset(offset).limit(limit).where(*filters)

    return sqlmodel_session.exec(statement).all()


async def update(
    *,
    sqlmodel_session: Session,
    retrieved_job: Job,
    job: UpdateJob,
) -> Job:
    if "location" in job.model_fields_set and job.location is not None:
        retrieved_location = await retrieve_location_by_id(
            sqlmodel_session=sqlmodel_session, job_id=retrieved_job.id, location_id=retrieved_job.location.id
        )

        await update_location(
            sqlmodel_session=sqlmodel_session, retrieved_location=retrieved_location, location=job.location
        )

    if "salary" in job.model_fields_set and job.salary is not None:
        retrieved_salary = await retrieve_salary_by_id(
            sqlmodel_session=sqlmodel_session, job_id=retrieved_job.id, salary_id=retrieved_job.salary.id
        )

        await update_salary(sqlmodel_session=sqlmodel_session, retrieved_salary=retrieved_salary, salary=job.salary)

    retrieved_job.sqlmodel_update(
        job.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude={"location", "salary"},
        ),
    )

    sqlmodel_session.add(retrieved_job)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_job)

    return retrieved_job


async def upsert(
    *,
    sqlmodel_session: Session,
    job: CreateJob | UpdateJob,
) -> Job:
    retrieved_job = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        job_id=job.id,
    )

    if retrieved_job:
        return await update(
            sqlmodel_session=sqlmodel_session,
            retrieved_job=retrieved_job,
            job=job,
        )

    return await create(sqlmodel_session=sqlmodel_session, job=job)


async def delete(*, sqlmodel_session: Session, retrieved_job: Job) -> Job:
    sqlmodel_session.delete(retrieved_job)
    sqlmodel_session.commit()

    return retrieved_job
