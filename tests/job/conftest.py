from datetime import datetime

import pytest
from sqlmodel import Session
from src.talentgate.job.models import Job, EmploymentType


@pytest.fixture
def make_job(sqlmodel_session: Session):
    def make(
        title = "job title",
        description = "job description",
        department = "job department",
        employment_type = EmploymentType.FULL_TIME,
        application_deadline = datetime.now(),
    ):
        job = Job(
            title=title,
            description=description,
            department=department,
            employment_type=employment_type,
            application_deadline=application_deadline
        )

        sqlmodel_session.add(job)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(job)

        return job

    return make

@pytest.fixture
def job(make_job):
    return make_job()
