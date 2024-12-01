from sqlmodel import Session

from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job
from src.talentgate.observer.models import Observer, CreateObserver, UpdateObserver
from src.talentgate.observer.service import create, retrieve_by_id, update, delete


async def test_create(sqlmodel_session: Session, employee: Employee, job: Job) -> None:
    new_observer = CreateObserver(
        job_id=job.id,
        employee_id=employee.id,
    )

    created_observer = await create(
        sqlmodel_session=sqlmodel_session, observer=new_observer
    )

    assert created_observer.employee_id == new_observer.employee_id
    assert created_observer.job_id == new_observer.job_id


async def test_retrieve_by_id(sqlmodel_session: Session, observer: Observer) -> None:
    retrieved_observer = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, observer_id=observer.id
    )

    assert retrieved_observer.id == observer.id
    assert retrieved_observer.employee_id == observer.employee_id
    assert retrieved_observer.job_id == observer.job_id


async def test_update(
    sqlmodel_session: Session, observer: Observer, employee: Employee, job: Job
) -> None:
    modified_observer = UpdateObserver(
        job_id=job.id,
        employee_id=employee.id,
    )

    updated_observer = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_observer=observer,
        observer=modified_observer,
    )

    assert updated_observer.employee_id == observer.employee_id
    assert updated_observer.job_id == observer.job_id


async def test_delete(sqlmodel_session: Session, observer: Observer) -> None:
    deleted_observer = await delete(
        sqlmodel_session=sqlmodel_session, retrieved_observer=observer
    )

    assert deleted_observer.employee_id == observer.employee_id
    assert deleted_observer.job_id == observer.job_id
