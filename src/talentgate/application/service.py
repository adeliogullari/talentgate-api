from collections.abc import Sequence
from io import BytesIO
from typing import Any

from minio import Minio
from minio.helpers import ObjectWriteResult
from sqlmodel import Session, select

from src.talentgate.application.models import (
    Application,
    ApplicationAddress,
    ApplicationLink,
    ApplicationQueryParameters,
    CreateApplication,
    CreateApplicationAddress,
    CreateApplicationLink,
    UpdateApplication,
    UpdateApplicationAddress,
    UpdateApplicationLink,
)


async def upload_resume(
    *,
    minio_client: Minio,
    object_name: str,
    data: BytesIO,
    length: int,
    content_type: str,
) -> ObjectWriteResult:
    return minio_client.put_object(
        bucket_name="resume",
        object_name=object_name,
        data=data,
        length=length,
        content_type=content_type,
    )


async def retrieve_resume(*, minio_client: Minio, object_name: str) -> bytes:
    response = None

    try:
        response = minio_client.get_object(
            bucket_name="resume",
            object_name=object_name,
        )
        data = response.data
    finally:
        if response:
            response.close()
            response.release_conn()

    return data


async def create_address(
    *,
    sqlmodel_session: Session,
    address: CreateApplicationAddress,
) -> ApplicationAddress:
    created_address = ApplicationAddress(
        **address.model_dump(exclude_unset=True, exclude_none=True),
    )

    sqlmodel_session.add(created_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_address)

    return created_address


async def retrieve_address_by_id(
    *,
    sqlmodel_session: Session,
    address_id: int,
) -> ApplicationAddress:
    statement: Any = select(ApplicationAddress).where(
        ApplicationAddress.id == address_id,
    )

    return sqlmodel_session.exec(statement).one_or_none()


async def update_address(
    *,
    sqlmodel_session: Session,
    retrieved_address: ApplicationAddress,
    address: UpdateApplicationAddress,
) -> ApplicationAddress:
    retrieved_address.sqlmodel_update(
        address.model_dump(exclude_none=True, exclude_unset=True),
    )

    sqlmodel_session.add(retrieved_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_address)

    return retrieved_address


async def create_link(
    *,
    sqlmodel_session: Session,
    link: CreateApplicationLink,
) -> ApplicationLink:
    created_link = ApplicationLink(
        **link.model_dump(exclude_unset=True, exclude_none=True),
    )

    sqlmodel_session.add(created_link)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_link)

    return created_link


async def retrieve_link_by_id(
    *,
    sqlmodel_session: Session,
    link_id: int,
) -> ApplicationLink:
    statement: Any = select(ApplicationLink).where(ApplicationLink.id == link_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def update_link(
    *,
    sqlmodel_session: Session,
    retrieved_link: ApplicationLink,
    link: UpdateApplicationLink,
) -> ApplicationLink:
    retrieved_link.sqlmodel_update(
        link.model_dump(exclude_none=True, exclude_unset=True),
    )

    sqlmodel_session.add(retrieved_link)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_link)

    return retrieved_link


async def upsert_link(
    *,
    sqlmodel_session: Session,
    link: CreateApplicationLink | UpdateApplicationLink,
) -> ApplicationLink:
    retrieved_link = await retrieve_link_by_id(
        sqlmodel_session=sqlmodel_session,
        link_id=link.id,
    )
    if retrieved_link:
        return await update_link(
            sqlmodel_session=sqlmodel_session,
            retrieved_link=retrieved_link,
            link=link,
        )
    return await create_link(sqlmodel_session=sqlmodel_session, link=link)


async def create(
    *,
    sqlmodel_session: Session,
    application: CreateApplication,
) -> Application:
    address = None
    if getattr(application, "address", None) is not None:
        address = await create_address(
            sqlmodel_session=sqlmodel_session,
            address=application.address,
        )

    links = []
    if (getattr(application, "links", None) or None) is not None:
        links = [await upsert_link(sqlmodel_session=sqlmodel_session, link=link) for link in application.links]

    created_application = Application(
        **application.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"address", "links"},
        ),
        address=address,
        links=links,
    )

    sqlmodel_session.add(created_application)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_application)

    return created_application


async def retrieve_by_id(
    *,
    sqlmodel_session: Session,
    application_id: int,
) -> Application:
    statement: Any = select(Application).where(Application.id == application_id)

    retrieved_application: Application = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application


async def retrieve_by_email(*, sqlmodel_session: Session, email: str) -> Application:
    statement: Any = select(Application).where(Application.email == email)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_phone(*, sqlmodel_session: Session, phone: str) -> Application:
    statement: Any = select(Application).where(Application.phone == phone)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_query_parameters(
    *,
    sqlmodel_session: Session,
    query_parameters: ApplicationQueryParameters,
) -> Sequence[Application]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Application, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit", "resume"},
            exclude_unset=True,
            exclude_none=True,
        )
    }

    statement: Any = select(Application).offset(offset).limit(limit).where(*filters)

    return sqlmodel_session.exec(statement).all()


async def update(
    *,
    sqlmodel_session: Session,
    retrieved_application: Application,
    application: UpdateApplication,
) -> Application:
    if getattr(application, "address", None) is not None:
        retrieved_application.address = await update_address(
            sqlmodel_session=sqlmodel_session,
            address=application.address,
        )

    if getattr(application, "links", None) is not None:
        retrieved_application.links = [
            await upsert_link(sqlmodel_session=sqlmodel_session, link=link) for link in application.links
        ]

    retrieved_application.sqlmodel_update(
        application.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude={"address", "links", "evaluations"},
        ),
    )

    sqlmodel_session.add(retrieved_application)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_application)

    return retrieved_application


async def delete(
    *,
    sqlmodel_session: Session,
    retrieved_application: Application,
) -> Application:
    sqlmodel_session.delete(retrieved_application)
    sqlmodel_session.commit()

    return retrieved_application
