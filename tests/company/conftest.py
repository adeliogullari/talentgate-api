import pytest
from sqlmodel import Session

from src.talentgate.company.models import Company
from src.talentgate.job.models import Job


@pytest.fixture
def make_company(sqlmodel_session: Session, job: Job):
    def make(
        name="test_company_name",
        overview="test_company_overview",
        jobs=None,
    ):
        if jobs is None:
            jobs = [job]

        company = Company(
            name=name, overview=overview, jobs=jobs
        )

        sqlmodel_session.add(company)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(company)

        return company

    return make


@pytest.fixture
def company(make_company):
    return make_company()
