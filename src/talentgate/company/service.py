from typing import Any, Sequence, List

from sqlalchemy import func
from sqlmodel import select, Session, or_, and_
from src.talentgate.company.models import (
    CompanyAddress,
    CompanyLocation,
    CompanyLink,
    Company,
    CreateAddress,
    CreateLocation,
    CreateLink,
    CreateCompany,
    CompanyQueryParameters,
    UpdateCompany,
)
from config import get_settings
from src.talentgate.job.models import Job, JobQueryParameters, JobLocation
from src.talentgate.employee import service as employee_service
from src.talentgate.employee.exceptions import (
    EmployeeIdNotFoundException as EmployeeIdNotFoundException,
)
from src.talentgate.job.exceptions import (
    ObserverAlreadyExistsException,
    ObserverNotFoundException,
)

settings = get_settings()


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
            *[Job.employment_type == et for et in query_parameters.employment_type]
        )
        filters.append(employment_filter)

    if query_parameters.location_type:
        location_filter = or_(
            *[JobLocation.type == lt for lt in query_parameters.location_type]
        )
        filters.append(location_filter)

    if query_parameters.department:
        department_filter = or_(
            *[Job.department == dept for dept in query_parameters.department]
        )
        filters.append(department_filter)

    if query_parameters.title:
        filters.append(
            func.lower(Job.title).ilike(f"%{query_parameters.title.lower()}%")
        )

    statement = (
        select(Job)
        .join(JobLocation)
        .where(and_(*filters))
        .offset(query_parameters.offset)
        .limit(query_parameters.limit)
    )

    retrieved_jobs = sqlmodel_session.exec(statement).all()
    return retrieved_jobs


async def retrieve_company_job(
    *,
    sqlmodel_session: Session,
    company_id: int,
    job_id: int,
) -> Job:
    statement: Any = (
        select(Job).where(Job.company_id == company_id).where(Job.id == job_id)
    )

    retrieved_job = sqlmodel_session.exec(statement).one()

    return retrieved_job


# OBSERVER Services
async def add_observer(
    *, sqlmodel_session: Session, retrieved_job: Job, observers: List[Any]
) -> None:
    for observer in observers:
        retrieved_employee = await employee_service.retrieve_by_id(
            sqlmodel_session=sqlmodel_session, employee_id=observer
        )

        if not retrieved_employee:
            raise EmployeeIdNotFoundException

        if retrieved_employee not in retrieved_job.observers:
            retrieved_job.observers.append(retrieved_employee)
        else:
            raise ObserverAlreadyExistsException

        sqlmodel_session.commit()
        sqlmodel_session.refresh(retrieved_job)

    return


async def delete_observer(
    *, sqlmodel_session: Session, retrieved_job: Job, employee_id: int
) -> None:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, employee_id=employee_id
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    if retrieved_employee in retrieved_job.observers:
        retrieved_job.observers.remove(retrieved_employee)
    else:
        raise ObserverNotFoundException

    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_job)

    return


async def create_address(
    *, sqlmodel_session: Session, address: CreateAddress
) -> CompanyAddress:
    created_address = CompanyAddress(
        **address.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_address)

    return created_address


async def create_location(
    *, sqlmodel_session: Session, location: CreateLocation
) -> CompanyLocation:
    address = None
    if getattr(location, "address", None) is not None:
        address = await create_address(
            sqlmodel_session=sqlmodel_session, address=location.address
        )

    created_location = CompanyLocation(
        **location.model_dump(
            exclude_unset=True, exclude_none=True, exclude={"address"}
        ),
        address=address,
    )

    sqlmodel_session.add(created_location)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_location)

    return created_location


async def create_link(*, sqlmodel_session: Session, link: CreateLink) -> CompanyLink:
    created_link = CompanyLink(**link.model_dump(exclude_unset=True, exclude_none=True))

    sqlmodel_session.add(created_link)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_link)

    return created_link


async def create(*, sqlmodel_session: Session, company: CreateCompany) -> Company:
    locations = None
    if getattr(company, "locations", None) is not None:
        locations = [
            await create_location(sqlmodel_session=sqlmodel_session, location=location)
            for location in company.locations
        ]

    links = None
    if getattr(company, "links", None) is not None:
        links = [
            await create_link(sqlmodel_session=sqlmodel_session, link=link)
            for link in company.links
        ]

    created_company = Company(
        **company.model_dump(exclude_unset=True, exclude_none=True),
        locations=locations,
        links=links,
    )

    sqlmodel_session.add(created_company)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_company)

    return created_company


async def retrieve_by_id(*, sqlmodel_session: Session, company_id: int) -> Company:
    statement: Any = select(Company).where(Company.id == company_id)

    retrieved_user = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_user


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: CompanyQueryParameters
) -> Sequence[Company]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Company, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        )
    }

    statement: Any = select(Company).offset(offset).limit(limit).where(*filters)

    retrieved_jobs = sqlmodel_session.exec(statement).all()

    return retrieved_jobs


async def update(
    *, sqlmodel_session: Session, retrieved_company: Company, company: UpdateCompany
) -> Company:
    retrieved_company.sqlmodel_update(
        company.model_dump(exclude_none=True, exclude_unset=True)
    )

    sqlmodel_session.add(retrieved_company)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_company)

    return retrieved_company


async def delete(*, sqlmodel_session: Session, retrieved_company: Company) -> Company:
    sqlmodel_session.delete(retrieved_company)
    sqlmodel_session.commit()

    return retrieved_company
