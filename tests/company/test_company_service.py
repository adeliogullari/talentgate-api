from sqlmodel import Session

from src.talentgate.company.models import Company, CreateCompany, UpdateCompany
from src.talentgate.company.service import (
    create,
    delete,
    retrieve_by_id,
    retrieve_company_job,
    retrieve_jobs_by_query_parameters,
    update,
    retrieve_by_name,
)

from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job, JobQueryParameters


async def test_retrieve_company_job(
    sqlmodel_session: Session,
    company: Company,
    job: Job,
) -> None:
    retrieved_company_job = await retrieve_company_job(
        sqlmodel_session=sqlmodel_session,
        company_id=company.id,
        job_id=job.id,
    )

    assert retrieved_company_job.id == job.id
    assert retrieved_company_job.company_id == company.id
    assert retrieved_company_job.title == job.title
    assert retrieved_company_job.description == job.description
    assert retrieved_company_job.department == job.department


async def test_create(sqlmodel_session: Session) -> None:
    new_company = CreateCompany(name="new_company", overview="new_company_overview")

    created_company = await create(
        sqlmodel_session=sqlmodel_session,
        company=new_company,
    )

    assert created_company.name == new_company.name
    assert created_company.overview == new_company.overview


async def test_retrieve_by_id(sqlmodel_session: Session, company: Company) -> None:
    retrieved_company = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        company_id=company.id,
    )

    assert retrieved_company.id == company.id
    assert retrieved_company.name == company.name
    assert retrieved_company.overview == company.overview


async def test_retrieve_by_name(sqlmodel_session: Session, company: Company) -> None:
    retrieved_company = await retrieve_by_name(
        sqlmodel_session=sqlmodel_session,
        name=company.name,
    )

    assert retrieved_company.name == company.name


async def test_update(sqlmodel_session: Session, company: Company) -> None:
    modified_company = UpdateCompany(
        name="updated_company",
        overview="updated_company_overview",
    )

    updated_company = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=company,
        company=modified_company,
    )

    assert updated_company.name == company.name
    assert updated_company.overview == company.overview


async def test_delete(sqlmodel_session: Session, company: Company) -> None:
    deleted_company = await delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=company,
    )

    assert deleted_company.name == company.name
    assert deleted_company.overview == company.overview
