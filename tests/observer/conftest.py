
import pytest
from sqlmodel import Session

from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job
from src.talentgate.observer.models import Observer


@pytest.fixture
def make_observer(sqlmodel_session: Session, employee: Employee, job: Job):
    def make(job_id=job.id, employee_id=employee.id):
        observer = Observer(job_id=job_id, employee_id=employee_id)

        sqlmodel_session.add(observer)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(observer)

        return observer

    return make


@pytest.fixture
def observer(make_observer):
    return make_observer()
