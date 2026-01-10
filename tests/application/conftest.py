import secrets
from typing import BinaryIO

import pytest
from minio import Minio
from sqlmodel import Session

from config import get_settings
from src.talentgate.application.models import (
    Application,
    ApplicationAddress,
    ApplicationLink,
)

settings = get_settings()


@pytest.fixture
def make_application_address(sqlmodel_session: Session):
    def make(**kwargs):
        address = ApplicationAddress(
            unit=kwargs.get("unit") or secrets.token_hex(12),
            street=kwargs.get("street") or secrets.token_hex(12),
            city=kwargs.get("city") or secrets.token_hex(12),
            state=kwargs.get("state") or secrets.token_hex(12),
            country=kwargs.get("country") or secrets.token_hex(12),
            postal_code=kwargs.get("postal_code") or secrets.randbelow(1000),
        )

        sqlmodel_session.add(address)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(address)

        return address

    return make


def application_address(make_application_address, request):
    param = getattr(request, "param", {})
    unit = param.get("unit", None)
    street = param.get("street", None)
    city = param.get("city", None)
    state = param.get("state", None)
    country = param.get("country", None)
    postal_code = param.get("postal_code", None)

    return make_application_address(
        unit=unit,
        street=street,
        city=city,
        state=state,
        country=country,
        postal_code=postal_code,
    )


@pytest.fixture
def make_application_link(sqlmodel_session: Session):
    def make(type: str = "type", url: str = "url"):
        link = ApplicationLink(type=type, url=url)

        sqlmodel_session.add(link)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(link)

        return link

    return make


@pytest.fixture
def application_link(make_application_link):
    return make_application_link()


@pytest.fixture
def make_resume(minio_client: Minio):
    def make(
        bucket_name: str = "resume",
        object_name: str = "resume",
        data: BinaryIO = b"resume",
        length: int = 0,
    ):
        return minio_client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data,
            length=length,
        )

    return make


@pytest.fixture
def resume(make_resume):
    return make_resume()


@pytest.fixture
def make_application(sqlmodel_session: Session):
    def make(**kwargs):
        application = Application(
            firstname=kwargs.get("firstname") or secrets.token_hex(12),
            lastname=kwargs.get("lastname") or secrets.token_hex(12),
            email=kwargs.get("email") or f"{secrets.token_hex(16)}@example.com",
            phone=kwargs.get("phone") or 1234,
            resume=kwargs.get("resume") or "resume",
        )

        sqlmodel_session.add(application)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(application)

        return application

    return make


@pytest.fixture
def application(make_application, request):
    param = getattr(request, "param", {})
    firstname = param.get("firstname", None)
    lastname = param.get("lastname", None)
    email = param.get("email", None)
    phone = param.get("phone", None)
    resume = param.get("resume", None)

    return make_application(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        resume=resume,
    )
