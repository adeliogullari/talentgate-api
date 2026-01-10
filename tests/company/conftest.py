import random
import secrets
from typing import Any
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.talentgate.company.models import (
    Company,
    CompanyLocationAddress,
    CompanyLocation,
    CompanyLink,
    CompanyEmployee,
)
from src.talentgate.job.models import Job
from src.talentgate.user.models import User


@pytest.fixture
def make_company_location_address(sqlmodel_session: Session) -> Any:
    def make(**kwargs) -> CompanyLocationAddress:
        company_location_address = CompanyLocationAddress(
            unit=kwargs.get("unit") or secrets.token_hex(12),
            street=kwargs.get("street") or secrets.token_hex(12),
            city=kwargs.get("city") or secrets.token_hex(12),
            state=kwargs.get("state") or secrets.token_hex(12),
            country=kwargs.get("country") or secrets.token_hex(12),
            postal_code=kwargs.get("postal_code") or secrets.token_hex(12),
        )

        sqlmodel_session.add(company_location_address)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(company_location_address)

        return company_location_address

    return make


@pytest.fixture
def company_location_address(make_company_location_address, request) -> Any:
    param = getattr(request, "param", {})
    unit = param.get("unit", None)
    street = param.get("street", None)
    city = param.get("city", None)
    state = param.get("state", None)
    country = param.get("country", None)
    postal_code = param.get("postal_code", None)

    return make_company_location_address(
        unit=unit, street=street, city=city, state=state, country=country, postal_code=postal_code
    )


@pytest.fixture
def make_company_location(sqlmodel_session: Session, company_location_address: CompanyLocationAddress) -> Any:
    def make(**kwargs) -> CompanyLocation:
        company_location = CompanyLocation(
            type=kwargs.get("type") or secrets.token_hex(12),
            latitude=kwargs.get("latitude") or random.uniform(0, 1),
            longitude=kwargs.get("longitude") or random.uniform(0, 1),
            address=kwargs.get("address") or company_location_address,
        )

        sqlmodel_session.add(company_location)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(company_location)

        return company_location

    return make


@pytest.fixture
def company_location(make_company_location, request) -> Any:
    param = getattr(request, "param", {})
    type = param.get("type", None)
    latitude = param.get("latitude", None)
    longitude = param.get("longitude", None)
    address = param.get("address", None)

    return make_company_location(type=type, latitude=latitude, longitude=longitude, address=address)


@pytest.fixture
def make_company_link(sqlmodel_session: Session) -> Any:
    def make(**kwargs) -> CompanyLink:
        company_link = CompanyLink(
            type=kwargs.get("type") or secrets.token_hex(12),
            url=kwargs.get("url") or secrets.token_hex(12),
        )

        sqlmodel_session.add(company_link)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(company_link)

        return company_link

    return make


@pytest.fixture
def company_link(make_company_link, request) -> Any:
    param = getattr(request, "param", {})
    type = param.get("type", None)
    url = param.get("url", None)

    return make_company_link(type=type, url=url)


@pytest.fixture
def make_company_employee(sqlmodel_session: Session, user: User) -> Any:
    def make(**kwargs) -> CompanyEmployee:
        company_employee = CompanyEmployee(
            title=kwargs.get("title") or secrets.token_hex(12),
            user=kwargs.get("user") or user,
        )

        sqlmodel_session.add(company_employee)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(company_employee)

        return company_employee

    return make


@pytest.fixture
def company_employee(make_company_employee, request) -> Any:
    param = getattr(request, "param", {})
    title = param.get("title", None)
    user = param.get("user", None)

    return make_company_employee(title=title, user=user)


@pytest.fixture
def make_company(
    sqlmodel_session: Session,
    company_location: CompanyLocation,
    company_link: CompanyLink,
    company_employee: CompanyEmployee,
    job: Job,
):
    def make(**kwargs):
        company = Company(
            name=kwargs.get("name") or secrets.token_hex(12),
            overview=kwargs.get("overview") or secrets.token_hex(12),
            logo=kwargs.get("logo") or str(uuid4()),
            locations=kwargs.get("locations") or [company_location],
            links=kwargs.get("links") or [company_link],
            employees=kwargs.get("employees") or [company_employee],
            jobs=kwargs.get("jobs") or [job],
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
    logo = param.get("logo", None)
    locations = param.get("locations", None)
    links = param.get("links", None)
    employees = param.get("employees", None)

    return make_company(
        name=name,
        overview=overview,
        logo=logo,
        locations=locations,
        links=links,
        employees=employees,
    )
