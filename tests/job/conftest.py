from datetime import datetime

import pytest
from sqlmodel import Session

from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job, EmploymentType


@pytest.fixture
def make_job(sqlmodel_session: Session, employee: Employee):
    def make(
        title="job title",
        description="job description",
        department="job department",
        employment_type=EmploymentType.FULL_TIME,
        application_deadline=datetime.now(),
        observers=None,
    ):
        if observers is None:
            observers = [employee]

        job = Job(
            title=title,
            description=description,
            department=department,
            employment_type=employment_type,
            application_deadline=application_deadline,
            observers=observers,
        )

        sqlmodel_session.add(job)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(job)

        return job

    return make


@pytest.fixture
def job(make_job):
    return make_job()
