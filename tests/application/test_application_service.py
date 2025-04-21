from datetime import datetime
from io import BytesIO

from minio import Minio
from sqlmodel import Session

from src.talentgate.application.models import (
    Application,
    CreateApplication,
    CreateResume,
    UpdateApplication,
)
from src.talentgate.application.service import (
    create,
    create_resume,
    delete,
    retrieve_by_email,
    retrieve_by_id,
    retrieve_by_phone,
    retrieve_resume,
    update,
)


async def test_create_resume(minio_client: Minio) -> None:
    await create_resume(
        minio_client=minio_client,
        object_name="resume.pdf",
        data=BytesIO(b"data"),
        length=len(b"data"),
    )


async def test_retrieve_resume(minio_client: Minio, resume) -> None:
    await retrieve_resume(minio_client=minio_client, object_name=resume.object_name)


async def test_create(sqlmodel_session: Session, minio_client: Minio) -> None:
    application = CreateApplication(
        firstname="firstname",
        lastname="lastname",
        email="email@gmail.com",
        phone="534654325",
        city="test_city",
        state="test_state",
        country="test_country",
        postal_code="32214",
        resume=CreateResume(name="resume", data=b"data"),
        earliest_start_date=datetime.now(),
    )

    created_application = await create(
        sqlmodel_session=sqlmodel_session,
        minio_client=minio_client,
        application=application,
    )

    assert created_application.email == application.email


async def test_retrieve_by_id(
    sqlmodel_session: Session,
    application: Application,
) -> None:
    retrieved_application = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        application_id=application.id,
    )

    assert retrieved_application.id == application.id


async def test_retrieve_by_email(
    sqlmodel_session: Session,
    application: Application,
) -> None:
    retrieved_application = await retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=application.email,
    )

    assert retrieved_application.email == application.email


async def test_retrieve_by_phone(
    sqlmodel_session: Session,
    application: Application,
) -> None:
    retrieved_application = await retrieve_by_phone(
        sqlmodel_session=sqlmodel_session,
        phone=application.phone,
    )

    assert retrieved_application.phone == application.phone


async def test_update(sqlmodel_session: Session, make_application) -> None:
    retrieved_application = make_application()

    application = UpdateApplication(
        firstname="updatedfirstname",
        lastname="updatedlastname",
        email="updatedemail@gmail.com",
        phone="updated534654325",
        resume="cv/test.pdf",
    )

    updated_application = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_application=retrieved_application,
        application=application,
    )

    assert application.firstname == updated_application.firstname


async def test_delete(sqlmodel_session, make_application) -> None:
    retrieved_application = make_application()

    deleted_application = await delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_application=retrieved_application,
    )

    assert retrieved_application.firstname == deleted_application.firstname
