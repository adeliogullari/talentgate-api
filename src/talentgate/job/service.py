from collections.abc import Sequence
from typing import Any

from sqlmodel import Session, select

from src.talentgate.job.models import (
    CreateJob,
    CreateJobAddress,
    CreateJobLocation,
    CreateSalary,
    Job,
    JobAddress,
    JobLocation,
    JobQueryParameters,
    JobSalary,
    UpdateJob,
    UpdateJobAddress,
    UpdateJobLocation,
    UpdateSalary,
)


async def create_address(
    *,
    sqlmodel_session: Session,
    address: CreateJobAddress,
) -> JobAddress:
    created_address = JobAddress(
        **address.model_dump(exclude_unset=True, exclude_none=True),
    )

    sqlmodel_session.add(created_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_address)

    return created_address


async def retrieve_address_by_id(
    *,
    sqlmodel_session: Session,
    address_id: int,
) -> JobAddress:
    statement: Any = select(JobAddress).where(JobAddress.id == address_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def update_address(
    *,
    sqlmodel_session: Session,
    retrieved_address: JobAddress,
    address: UpdateJobAddress,
) -> JobAddress:
    retrieved_address.sqlmodel_update(
        address.model_dump(exclude_none=True, exclude_unset=True),
    )

    sqlmodel_session.add(retrieved_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_address)

    return retrieved_address


async def upsert_address(
    *,
    sqlmodel_session: Session,
    address: CreateJobAddress | UpdateJobAddress,
) -> JobAddress:
    retrieved_address = await retrieve_address_by_id(
        sqlmodel_session=sqlmodel_session,
        address_id=address.id,
    )
    if retrieved_address:
        return await update_address(
            sqlmodel_session=sqlmodel_session,
            retrieved_address=retrieved_address,
            address=address,
        )
    return await create_address(sqlmodel_session=sqlmodel_session, address=address)


async def create_location(
    *,
    sqlmodel_session: Session,
    location: CreateJobLocation,
) -> JobLocation:
    address = None
    if getattr(location, "address", None) is not None:
        address = await create_address(
            sqlmodel_session=sqlmodel_session,
            address=location.address,
        )

    created_location = JobLocation(
        **location.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"address"},
        ),
        address=address,
    )

    sqlmodel_session.add(created_location)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_location)

    return created_location


async def retrieve_location_by_id(
    *,
    sqlmodel_session: Session,
    location_id: int,
) -> JobLocation:
    statement: Any = select(JobLocation).where(JobLocation.id == location_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def update_location(
    *,
    sqlmodel_session: Session,
    retrieved_location: JobLocation,
    location: UpdateJobLocation,
) -> JobLocation:
    if getattr(location, "address", None) is not None:
        retrieved_location.address = await upsert_address(
            sqlmodel_session=sqlmodel_session,
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


async def upsert_location(
    *,
    sqlmodel_session: Session,
    location: CreateJobLocation | UpdateJobLocation,
) -> JobLocation:
    retrieved_location = await retrieve_location_by_id(
        sqlmodel_session=sqlmodel_session,
        location_id=location.id,
    )

    if retrieved_location:
        return await update_location(
            sqlmodel_session=sqlmodel_session,
            retrieved_location=retrieved_location,
            location=location,
        )

    return await create_location(sqlmodel_session=sqlmodel_session, location=location)


async def create_salary(
    *,
    sqlmodel_session: Session,
    salary: CreateSalary,
) -> JobSalary:
    created_salary = JobSalary(
        **salary.model_dump(exclude_unset=True, exclude_none=True),
    )

    sqlmodel_session.add(created_salary)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_salary)

    return created_salary


async def retrieve_salary_by_id(
    *,
    sqlmodel_session: Session,
    salary_id: int,
) -> JobSalary:
    statement: Any = select(JobSalary).where(JobSalary.id == salary_id)

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


async def upsert_salary(
    *,
    sqlmodel_session: Session,
    salary: CreateSalary | UpdateSalary,
) -> JobSalary:
    retrieved_salary = await retrieve_salary_by_id(
        sqlmodel_session=sqlmodel_session,
        salary_id=salary.id,
    )
    if retrieved_salary:
        return await update_salary(
            sqlmodel_session=sqlmodel_session,
            retrieved_salary=retrieved_salary,
            salary=salary,
        )
    return await create_salary(sqlmodel_session=sqlmodel_session, salary=salary)


async def create(*, sqlmodel_session: Session, job: CreateJob) -> Job:
    location = None
    if getattr(job, "location", None) is not None:
        location = await create_location(
            sqlmodel_session=sqlmodel_session,
            location=job.location,
        )

    salary = None
    if getattr(job, "salary", None) is not None:
        salary = await create_salary(
            sqlmodel_session=sqlmodel_session,
            salary=job.salary,
        )

    created_job = Job(
        **job.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"location", "salary"},
        ),
        location=location,
        salary=salary,
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
    if getattr(job, "location", None) is not None:
        retrieved_job.location = await upsert_location(
            sqlmodel_session=sqlmodel_session,
            location=job.location,
        )

    if getattr(job, "salary", None) is not None:
        retrieved_job.salary = await upsert_salary(
            sqlmodel_session=sqlmodel_session,
            salary=job.salary,
        )

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
