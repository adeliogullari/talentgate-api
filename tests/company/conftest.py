import secrets

import pytest
from sqlmodel import Session

from src.talentgate.company.models import (
    Company,
    CompanyAddress,
    CompanyLocation,
    CompanyLocationType,
)
from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job


@pytest.fixture
def address(sqlmodel_session: Session):
    company_location_address = CompanyAddress(
        unit=None,
        street=None,
        city=None,
        state=None,
        country=None,
        postal_code=None,
    )

    sqlmodel_session.add(company_location_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(company_location_address)

    return company_location_address


@pytest.fixture
def location(sqlmodel_session: Session, address: CompanyAddress):
    company_location = CompanyLocation(
        type=CompanyLocationType.OFFICE,
        latitude=0,
        longtitude=0,
        address=address,
    )

    sqlmodel_session.add(company_location)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(company_location)

    return company_location


@pytest.fixture
def make_company(
    sqlmodel_session: Session,
    job: Job,
    employee: Employee,
    location: CompanyLocation,
):
    def make(**kwargs):
        company = Company(
            name=kwargs.get("firstname") or secrets.token_hex(12),
            overview=kwargs.get("overview") or secrets.token_hex(12),
            employees=kwargs.get("employees") or [employee],
            locations=kwargs.get("locations") or [location],
            jobs=[job],
        )

        sqlmodel_session.add(company)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(company)

        return company

    return make


@pytest.fixture
def company(make_company, request):
    param = getattr(request, "param", {})
    name = param.get("name", None)
    overview = param.get("overview", None)
    employees = param.get("employees", None)
    locations = param.get("locations", None)

    return make_company(
        name=name,
        overview=overview,
        employees=employees,
        locations=locations,
    )
