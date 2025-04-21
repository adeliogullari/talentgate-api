from collections.abc import Sequence
from io import BytesIO
from typing import Any

from minio import Minio
from minio.helpers import ObjectWriteResult
from sqlmodel import Session, select

from src.talentgate.application.models import (
    Application,
    ApplicationAddress,
    ApplicationEvaluation,
    ApplicationLink,
    ApplicationQueryParameters,
    CreateAddress,
    CreateApplication,
    CreateEvaluation,
    CreateLink,
    RetrievedResume,
    UpdateAddress,
    UpdateApplication,
    UpdateEvaluation,
    UpdateLink,
)


async def create_resume(
    *,
    minio_client: Minio,
    object_name: str,
    data: BytesIO,
    length: int,
) -> ObjectWriteResult:
    return minio_client.put_object(
        bucket_name="resume",
        object_name=object_name,
        data=data,
        length=length,
    )


async def retrieve_resume(*, minio_client: Minio, object_name: str) -> RetrievedResume:
    response = None
    try:
        response = minio_client.get_object(
            bucket_name="resume",
            object_name=object_name,
        )
    finally:
        if response:
            response.close()
            response.release_conn()

    return RetrievedResume(name=object_name, data=response.data)


async def create_address(
    *,
    sqlmodel_session: Session,
    address: CreateAddress,
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
    address: UpdateAddress,
) -> ApplicationAddress:
    retrieved_address.sqlmodel_update(
        address.model_dump(exclude_none=True, exclude_unset=True),
    )

    sqlmodel_session.add(retrieved_address)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_address)

    return retrieved_address


async def upsert_address(
    *,
    sqlmodel_session: Session,
    address: CreateAddress | UpdateAddress,
) -> ApplicationAddress:
    retrieved_address = await retrieve_address_by_id(
        sqlmodel_session=sqlmodel_session,
        address_id=address.id,
    )
    if retrieved_address:
        return await update_address(
            sqlmodel_session=sqlmodel_session,
            retrieved_address=retrieved_address,
            address=address,
        )
    return await create_address(sqlmodel_session=sqlmodel_session, address=address)


async def create_link(
    *,
    sqlmodel_session: Session,
    link: CreateLink,
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
    link: UpdateLink,
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
    link: CreateLink | UpdateLink,
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


async def create_evaluation(
    *,
    sqlmodel_session: Session,
    evaluation: CreateEvaluation,
) -> ApplicationEvaluation:
    created_evaluation = ApplicationEvaluation(
        **evaluation.model_dump(exclude_unset=True, exclude_none=True),
    )

    sqlmodel_session.add(created_evaluation)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_evaluation)

    return created_evaluation


async def retrieve_evaluation_by_id(
    *,
    sqlmodel_session: Session,
    evaluation_id: int,
) -> ApplicationEvaluation:
    statement: Any = select(ApplicationEvaluation).where(
        ApplicationEvaluation.id == evaluation_id,
    )

    return sqlmodel_session.exec(statement).one_or_none()


async def update_evaluation(
    *,
    sqlmodel_session: Session,
    retrieved_evaluation: ApplicationEvaluation,
    evaluation: UpdateEvaluation,
) -> ApplicationEvaluation:
    retrieved_evaluation.sqlmodel_update(
        evaluation.model_dump(exclude_none=True, exclude_unset=True),
    )

    sqlmodel_session.add(retrieved_evaluation)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_evaluation)

    return retrieved_evaluation


async def upsert_evaluation(
    *,
    sqlmodel_session: Session,
    evaluation: CreateEvaluation | UpdateEvaluation,
) -> ApplicationEvaluation:
    retrieved_evaluation = await retrieve_evaluation_by_id(
        sqlmodel_session=sqlmodel_session,
        evaluation_id=evaluation.id,
    )
    if retrieved_evaluation:
        return await update_evaluation(
            sqlmodel_session=sqlmodel_session,
            retrieved_evaluation=retrieved_evaluation,
            evaluation=evaluation,
        )
    return await create_evaluation(
        sqlmodel_session=sqlmodel_session,
        evaluation=evaluation,
    )


async def create(
    *,
    sqlmodel_session: Session,
    minio_client: Minio,
    application: CreateApplication,
) -> Application:
    resume = None
    if getattr(application, "resume", None) is not None:
        resume = await create_resume(
            minio_client=minio_client,
            object_name=application.resume.name,
            data=BytesIO(application.resume.data),
            length=len(application.resume.data),
        )

    address = None
    if getattr(application, "address", None) is not None:
        address = await upsert_address(
            sqlmodel_session=sqlmodel_session,
            address=application.address,
        )

    links = []
    if (getattr(application, "links", None) or None) is not None:
        links = [
            await upsert_link(sqlmodel_session=sqlmodel_session, link=link)
            for link in application.links
        ]

    evaluations = []
    if (getattr(application, "evaluations", None) or None) is not None:
        evaluations = [
            await upsert_evaluation(
                sqlmodel_session=sqlmodel_session,
                evaluation=evaluation,
            )
            for evaluation in application.evaluations
        ]

    created_application = Application(
        **application.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"resume", "address", "links", "evaluations"},
        ),
        resume=resume.object_name,
        address=address,
        links=links,
        evaluations=evaluations,
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
        retrieved_application.address = await upsert_address(
            sqlmodel_session=sqlmodel_session,
            address=application.address,
        )

    if getattr(application, "links", None) is not None:
        retrieved_application.links = [
            await upsert_link(sqlmodel_session=sqlmodel_session, link=link)
            for link in application.links
        ]

    if getattr(application, "evaluations", None) is not None:
        retrieved_application.evaluations = [
            await upsert_evaluation(
                sqlmodel_session=sqlmodel_session,
                evaluation=evaluation,
            )
            for evaluation in application.evaluations
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
