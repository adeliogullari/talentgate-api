from typing import Any, Sequence, List
from sqlmodel import select, Session
from src.talentgate.company.models import (
    Company,
    CreateCompany,
    CompanyQueryParameters,
    UpdateCompany,
)
from config import get_settings
from src.talentgate.job.models import Job
from src.talentgate.employee import service as employee_service
from src.talentgate.employee.exceptions import (
    IdNotFoundException as EmployeeIdNotFoundException,
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
    query_parameters: CompanyQueryParameters,
    company_id: int,
) -> Sequence[Job]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Job, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        )
    }

    statement: Any = (
        select(Job)
        .where(Job.company_id == company_id)
        .offset(offset)
        .limit(limit)
        .where(*filters)
    )

    retrieved_jobs = sqlmodel_session.exec(statement).all()

    return retrieved_jobs


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


# COMPANY Services
async def create(*, sqlmodel_session: Session, company: CreateCompany) -> Company:
    created_company = Company(
        **company.model_dump(exclude_unset=True, exclude_none=True)
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
    retrieved_company.sqlmodel_update(company)

    sqlmodel_session.add(retrieved_company)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_company)

    return retrieved_company


async def delete(*, sqlmodel_session: Session, retrieved_company: Company) -> Company:
    sqlmodel_session.delete(retrieved_company)
    sqlmodel_session.commit()

    return retrieved_company
