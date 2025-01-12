from sqlmodel import Session

from src.talentgate.company.models import Company, CreateCompany, UpdateCompany
from src.talentgate.company.service import (
    create,
    retrieve_by_id,
    update,
    delete,
    add_observer,
    delete_observer,
)
from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job
from tests.employee.conftest import make_employee


async def test_add_observer(
    sqlmodel_session: Session, job: Job, employee: Employee, make_employee
) -> None:
    created_observer = make_employee()

    await add_observer(
        sqlmodel_session=sqlmodel_session,
        retrieved_job=job,
        observers=[created_observer.id],
    )

    assert job.observers[1].id == created_observer.id


async def test_delete_observer(
    sqlmodel_session: Session, job: Job, employee: Employee
) -> None:
    await delete_observer(
        sqlmodel_session=sqlmodel_session, retrieved_job=job, employee_id=employee.id
    )

    assert len(job.observers) == 0


async def test_create(sqlmodel_session: Session) -> None:
    new_company = CreateCompany(name="new_company", overview="new_company_overview")

    created_company = await create(
        sqlmodel_session=sqlmodel_session, company=new_company
    )

    assert created_company.name == new_company.name
    assert created_company.overview == new_company.overview


async def test_retrieve_by_id(sqlmodel_session: Session, company: Company) -> None:
    retrieved_company = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=company.id
    )

    assert retrieved_company.id == company.id
    assert retrieved_company.name == company.name
    assert retrieved_company.overview == company.overview


async def test_update(sqlmodel_session: Session, company: Company) -> None:
    modified_company = UpdateCompany(
        name="updated_company", overview="updated_company_overview"
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
        sqlmodel_session=sqlmodel_session, retrieved_company=company
    )

    assert deleted_company.name == company.name
    assert deleted_company.overview == company.overview
