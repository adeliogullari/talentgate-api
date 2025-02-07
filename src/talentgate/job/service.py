from typing import Any, Union, Sequence
from sqlmodel import select, Session

from src.talentgate.job.models import (
    Job,
    CreateJob,
    UpdateJob,
    JobQueryParameters,
    JobLocation,
    CreateAddress,
    UpdateAddress,
    JobAddress,
    CreateLocation,
    UpdateLocation,
)


async def create_address(
    *, sqlmodel_session: Session, address: CreateAddress
) -> JobAddress:
    created_address = JobAddress(
        **address.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_address)

    return created_address


async def retrieve_address_by_id(
    *, sqlmodel_session: Session, address_id: int
) -> JobAddress:
    statement: Any = select(JobAddress).where(JobAddress.id == address_id)

    retrieved_address = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_address


async def update_address(
    *,
    sqlmodel_session: Session,
    retrieved_address: JobAddress,
    address: UpdateAddress,
) -> JobAddress:
    retrieved_address.sqlmodel_update(
        address.model_dump(exclude_none=True, exclude_unset=True)
    )

    sqlmodel_session.add(retrieved_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_address)

    return retrieved_address


async def upsert_address(
    *,
    sqlmodel_session: Session,
    address: Union[CreateAddress, UpdateAddress],
) -> JobAddress:
    retrieved_address = await retrieve_address_by_id(
        sqlmodel_session=sqlmodel_session, address_id=address.id
    )
    if retrieved_address:
        return await update_address(
            sqlmodel_session=sqlmodel_session,
            retrieved_address=retrieved_address,
            address=address,
        )
    return await create_address(sqlmodel_session=sqlmodel_session, address=address)


async def create_location(
    *, sqlmodel_session: Session, location: CreateLocation
) -> JobLocation:
    address = None
    if getattr(location, "address", None) is not None:
        address = await create_address(
            sqlmodel_session=sqlmodel_session, address=location.address
        )

    created_location = JobLocation(
        **location.model_dump(
            exclude_unset=True, exclude_none=True, exclude={"address"}
        ),
        address=address,
    )

    sqlmodel_session.add(created_location)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_location)

    return created_location


async def retrieve_location_by_id(
    *, sqlmodel_session: Session, location_id: int
) -> JobLocation:
    statement: Any = select(JobLocation).where(JobLocation.id == location_id)

    retrieved_location = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_location


async def update_location(
    *,
    sqlmodel_session: Session,
    retrieved_location: JobLocation,
    location: UpdateLocation,
) -> JobLocation:
    if getattr(location, "address", None) is not None:
        retrieved_location.address = await upsert_address(
            sqlmodel_session=sqlmodel_session, address=location.address
        )

    retrieved_location.sqlmodel_update(
        location.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude={"address"},
        )
    )

    sqlmodel_session.add(retrieved_location)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_location)

    return retrieved_location


async def upsert_location(
    *,
    sqlmodel_session: Session,
    location: Union[CreateLocation, UpdateLocation],
) -> JobLocation:
    retrieved_location = await retrieve_location_by_id(
        sqlmodel_session=sqlmodel_session, location_id=location.id
    )

    if retrieved_location:
        return await update_location(
            sqlmodel_session=sqlmodel_session,
            retrieved_location=retrieved_location,
            location=location,
        )

    return await create_location(sqlmodel_session=sqlmodel_session, location=location)


async def create(*, sqlmodel_session: Session, job: CreateJob) -> Job:
    location = None
    if getattr(job, "location", None) is not None:
        location = await create_location(
            sqlmodel_session=sqlmodel_session, location=job.location
        )

    created_job = Job(
        **job.model_dump(exclude_unset=True, exclude_none=True, exclude={"location"}),
        location=location,
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
    if getattr(job, "location", None) is not None:
        retrieved_job.location = await upsert_location(
            sqlmodel_session=sqlmodel_session, location=job.location
        )

    retrieved_job.sqlmodel_update(
        job.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude={"location"},
        )
    )

    sqlmodel_session.add(retrieved_job)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_job)

    return retrieved_job


async def delete(*, sqlmodel_session: Session, retrieved_job: Job) -> Job:
    sqlmodel_session.delete(retrieved_job)
    sqlmodel_session.commit()

    return retrieved_job
