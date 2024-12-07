from sqlmodel import Session

from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job, CreateJob, UpdateJob, EmploymentType
from src.talentgate.job.service import (
    create,
    retrieve_by_id,
    update,
    delete,
    add_observers,
    retrieve_observers_of_single_job,
    retrieve_observer_by_job_and_employee,
    delete_observer,
)


async def test_add_observers(sqlmodel_session: Session, employee: Employee) -> None:
    job = Job(title="Test Job")
    sqlmodel_session.add(job)
    sqlmodel_session.commit()

    created_observer = await add_observers(
        sqlmodel_session=sqlmodel_session, job=job, employees=[employee]
    )

    assert created_observer[0].job_id == job.id
    assert created_observer[0].employee_id == employee.id


async def test_retrieve_observer_by_job_and_employee(
    sqlmodel_session: Session, job: Job, employee: Employee
) -> None:
    retrieved_observer = await retrieve_observer_by_job_and_employee(
        sqlmodel_session=sqlmodel_session, job=job, employee=employee
    )

    assert retrieved_observer.job_id == job.id
    assert retrieved_observer.employee_id == employee.id


async def test_retrieve_observers_of_single_job(
    sqlmodel_session: Session, job: Job
) -> None:
    retrieved_observers = await retrieve_observers_of_single_job(job=job)

    assert retrieved_observers[0].job_id == job.id
    assert retrieved_observers[0].employee_id == job.observers[0].id


async def test_delete_observer(
    sqlmodel_session: Session, job: Job, employee: Employee
) -> None:
    deleted_observer = await delete_observer(
        sqlmodel_session=sqlmodel_session, job=job, employee=employee
    )

    assert deleted_observer.job_id == job.id
    assert deleted_observer.employee_id == employee.id


async def test_create(sqlmodel_session: Session) -> None:
    new_job = CreateJob(
        title="created job title",
        description="created job description",
        department="created job department",
        employment_type=EmploymentType.PART_TIME,
    )

    created_job = await create(sqlmodel_session=sqlmodel_session, job=new_job)

    assert created_job.title == new_job.title
    assert created_job.description == new_job.description
    assert created_job.department == new_job.department


async def test_retrieve_by_id(sqlmodel_session: Session, job: Job) -> None:
    retrieved_job = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job.id
    )

    assert retrieved_job.id == job.id
    assert retrieved_job.title == job.title
    assert retrieved_job.description == job.description
    assert retrieved_job.department == job.department


async def test_update(sqlmodel_session: Session, job: Job) -> None:
    modified_job = UpdateJob(
        title="updated job title",
        description="updated job description",
        department="updated job department",
        employment_type=EmploymentType.PART_TIME,
    )

    updated_job = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_job=job,
        job=modified_job,
    )

    assert updated_job.title == job.title
    assert updated_job.description == job.description
    assert updated_job.department == job.department


async def test_delete(sqlmodel_session: Session, job: Job) -> None:
    deleted_job = await delete(sqlmodel_session=sqlmodel_session, retrieved_job=job)

    assert deleted_job.title == job.title
    assert deleted_job.description == job.description
    assert deleted_job.department == job.department
