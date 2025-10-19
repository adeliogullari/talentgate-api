from collections.abc import Sequence
from io import BytesIO
from typing import Any

from fastapi import BackgroundTasks
from minio import Minio
from minio.helpers import ObjectWriteResult
from sqlalchemy import func
from sqlmodel import Session, and_, or_, select

from config import get_settings
from src.talentgate.company.models import (
    Company,
    CompanyAddress,
    CompanyLink,
    CompanyLocation,
    CompanyQueryParameters,
    CreateAddress,
    CreateCompany,
    CreateLink,
    CreateLocation,
    UpdateAddress,
    UpdateCompany,
    UpdateLink,
    UpdateLocation,
)
from src.talentgate.email import service as email_service
from src.talentgate.email.client import EmailClient
from src.talentgate.employee import service as employee_service
from src.talentgate.job.models import Job, JobLocation, JobQueryParameters

settings = get_settings()


async def upload_logo(
    *,
    minio_client: Minio,
    object_name: str,
    data: BytesIO,
    length: int,
    content_type: str,
) -> ObjectWriteResult:
    return minio_client.put_object(
        bucket_name="logo",
        object_name=object_name,
        data=data,
        length=length,
        content_type=content_type,
    )


async def retrieve_logo(*, minio_client: Minio, object_name: str) -> bytes:
    response = None

    try:
        response = minio_client.get_object(
            bucket_name="logo",
            object_name=object_name,
        )
        data = response.data
    finally:
        if response:
            response.close()
            response.release_conn()

    return data


async def create_address(
    *,
    sqlmodel_session: Session,
    address: CreateAddress,
) -> CompanyAddress:
    created_address = CompanyAddress(
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
) -> CompanyAddress:
    statement: Any = select(CompanyAddress).where(CompanyAddress.id == address_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def update_address(
    *,
    sqlmodel_session: Session,
    retrieved_address: CompanyAddress,
    address: UpdateAddress,
) -> CompanyAddress:
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
    address: CreateAddress | UpdateAddress,
) -> CompanyAddress:
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
    location: CreateLocation,
) -> CompanyLocation:
    address = None
    if getattr(location, "address", None) is not None:
        address = await create_address(
            sqlmodel_session=sqlmodel_session,
            address=location.address,
        )

    created_location = CompanyLocation(
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
) -> CompanyLocation:
    statement: Any = select(CompanyLocation).where(CompanyLocation.id == location_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def update_location(
    *,
    sqlmodel_session: Session,
    retrieved_location: CompanyLocation,
    location: UpdateLocation,
) -> CompanyLocation:
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
    location: CreateLocation | UpdateLocation,
) -> CompanyLocation:
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


async def create_link(*, sqlmodel_session: Session, link: CreateLink) -> CompanyLink:
    created_link = CompanyLink(**link.model_dump(exclude_unset=True, exclude_none=True))

    sqlmodel_session.add(created_link)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_link)

    return created_link


async def retrieve_link_by_id(
    *,
    sqlmodel_session: Session,
    link_id: int,
) -> CompanyLink:
    statement: Any = select(CompanyLink).where(CompanyLink.id == link_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def update_link(
    *,
    sqlmodel_session: Session,
    retrieved_link: CompanyLink,
    link: UpdateLink,
) -> CompanyLink:
    retrieved_link.sqlmodel_update(
        link.model_dump(exclude_none=True, exclude_unset=True),
    )

    sqlmodel_session.add(retrieved_link)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_link)

    return retrieved_link


async def upsert_link(
    *,
    sqlmodel_session: Session,
    link: CreateLink | UpdateLink,
) -> CompanyLink:
    retrieved_link = await retrieve_link_by_id(
        sqlmodel_session=sqlmodel_session,
        link_id=link.id,
    )
    if retrieved_link:
        return await update_link(
            sqlmodel_session=sqlmodel_session,
            retrieved_link=retrieved_link,
            link=link,
        )
    return await create_link(sqlmodel_session=sqlmodel_session, link=link)


# JOB Services
async def retrieve_jobs_by_query_parameters(
    *,
    sqlmodel_session: Session,
    query_parameters: JobQueryParameters,
    company_id: int,
) -> Sequence[Job]:
    filters = [Job.company_id == company_id]

    if query_parameters.employment_type:
        employment_filter = or_(
            *[Job.employment_type == et for et in query_parameters.employment_type],
        )
        filters.append(employment_filter)

    if query_parameters.location_type:
        location_filter = or_(
            *[JobLocation.type == lt for lt in query_parameters.location_type],
        )
        filters.append(location_filter)

    if query_parameters.department:
        department_filter = or_(
            *[Job.department == dept for dept in query_parameters.department],
        )
        filters.append(department_filter)

    if query_parameters.title:
        filters.append(
            func.lower(Job.title).ilike(f"%{query_parameters.title.lower()}%"),
        )

    statement = (
        select(Job)
        .join(JobLocation)
        .where(and_(*filters))
        .offset(query_parameters.offset)
        .limit(query_parameters.limit)
    )

    return sqlmodel_session.exec(statement).all()


async def retrieve_company_job(
    *,
    sqlmodel_session: Session,
    company_id: int,
    job_id: int,
) -> Job:
    statement: Any = (
        select(Job).where(Job.company_id == company_id).where(Job.id == job_id)
    )

    return sqlmodel_session.exec(statement).one()


async def create(*, sqlmodel_session: Session, company: CreateCompany) -> Company:
    locations = []
    if getattr(company, "locations", None) is not None:
        locations = [
            await upsert_location(sqlmodel_session=sqlmodel_session, location=location)
            for location in company.locations
        ]

    links = []
    if getattr(company, "links", None) is not None:
        links = [
            await upsert_link(sqlmodel_session=sqlmodel_session, link=link)
            for link in company.links
        ]

    employees = []
    if getattr(company, "employees", None) is not None:
        employees = [
            await employee_service.upsert(
                sqlmodel_session=sqlmodel_session,
                employee=employee,
            )
            for employee in company.employees
        ]

    created_company = Company(
        **company.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"locations", "links", "employees"},
        ),
        locations=locations,
        links=links,
        employees=employees,
    )

    sqlmodel_session.add(created_company)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_company)

    return created_company


async def retrieve_by_id(*, sqlmodel_session: Session, company_id: int) -> Company:
    statement: Any = select(Company).where(Company.id == company_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_name(*, sqlmodel_session: Session, name: str) -> Company:
    statement: Any = select(Company).where(Company.name == name)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_query_parameters(
    *,
    sqlmodel_session: Session,
    query_parameters: CompanyQueryParameters,
) -> Sequence[Company]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Company, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"},
            exclude_unset=True,
            exclude_none=True,
        )
    }

    statement: Any = select(Company).offset(offset).limit(limit).where(*filters)

    return sqlmodel_session.exec(statement).all()


async def update(
    *,
    sqlmodel_session: Session,
    retrieved_company: Company,
    company: UpdateCompany,
) -> Company:
    if getattr(company, "locations", None) is not None:
        retrieved_company.locations = [
            await upsert_location(sqlmodel_session=sqlmodel_session, location=location)
            for location in company.locations
        ]

    if getattr(company, "links", None) is not None:
        retrieved_company.links = [
            await upsert_link(sqlmodel_session=sqlmodel_session, link=link)
            for link in company.links
        ]

    if getattr(company, "employees", None) is not None:
        retrieved_company.employees = [
            await employee_service.upsert(
                sqlmodel_session=sqlmodel_session,
                employee=employee,
            )
            for employee in company.employees
        ]

    retrieved_company.sqlmodel_update(
        company.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude={"locations", "links", "employees"},
        ),
    )

    sqlmodel_session.add(retrieved_company)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_company)

    return retrieved_company


async def delete(*, sqlmodel_session: Session, retrieved_company: Company) -> Company:
    sqlmodel_session.delete(retrieved_company)
    sqlmodel_session.commit()

    return retrieved_company


async def send_onboarding_email(
    *,
    email_client: EmailClient,
    background_tasks: BackgroundTasks,
    context: dict,
    from_addr: str | None = None,
    to_addrs: str | Sequence[str] | None = None,
) -> None:
    body = email_service.load_template(
        file="src/talentgate/company/templates/onboarding.txt"
    )

    html = email_service.load_template(
        file="src/talentgate/company/templates/onboarding.html"
    )

    background_tasks.add_task(
        email_service.send_email,
        email_client,
        "Employee Onboarding",
        body,
        html,
        context,
        from_addr,
        to_addrs,
    )
