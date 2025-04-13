import uuid
from io import BytesIO
from typing import Any, Sequence, List, Union
from minio import Minio
from sqlmodel import select, Session
from src.talentgate.application.models import (
    Application,
    ApplicationQueryParameters,
    CreateApplication,
    UpdateApplication,
    ApplicationEvaluation,
    RetrievedResume,
    CreateEvaluation,
    UpdateEvaluation,
    ApplicationLink,
    UpdateLink,
    CreateLink,
)


async def create_resume(
    *, minio_client: Minio, object_name: str, data: BytesIO, length: int
):
    return minio_client.put_object(
        bucket_name="resume",
        object_name=object_name,
        data=data,
        length=length,
    )


async def retrieve_resume(*, minio_client: Minio, object_name: str):
    response = None
    try:
        response = minio_client.get_object(
            bucket_name="resume", object_name=object_name
        )
    finally:
        if response:
            response.close()
            response.release_conn()

    return RetrievedResume(name=object_name, data=response.data)


async def create_link(
    *, sqlmodel_session: Session, link: CreateLink
) -> ApplicationLink:
    created_link = ApplicationLink(
        **link.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_link)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_link)

    return created_link


async def retrieve_link_by_id(
    *, sqlmodel_session: Session, link_id: int
) -> ApplicationLink:
    statement: Any = select(ApplicationLink).where(ApplicationLink.id == link_id)

    retrieved_evaluation = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_evaluation


async def update_link(
    *,
    sqlmodel_session: Session,
    retrieved_link: ApplicationLink,
    link: UpdateLink,
) -> ApplicationLink:
    retrieved_link.sqlmodel_update(
        link.model_dump(exclude_none=True, exclude_unset=True)
    )

    sqlmodel_session.add(retrieved_link)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_link)

    return retrieved_link


async def upsert_link(
    *, sqlmodel_session: Session, link: Union[CreateLink, UpdateLink]
) -> ApplicationLink:
    retrieved_link = await retrieve_link_by_id(
        sqlmodel_session=sqlmodel_session, link_id=link.id
    )
    if retrieved_link:
        return await update_link(
            sqlmodel_session=sqlmodel_session,
            retrieved_link=retrieved_link,
            link=link,
        )
    return await create_link(sqlmodel_session=sqlmodel_session, link=link)


async def create_evaluation(
    *, sqlmodel_session: Session, evaluation: CreateEvaluation
) -> ApplicationEvaluation:
    created_evaluation = ApplicationEvaluation(
        **evaluation.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_evaluation)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_evaluation)

    return created_evaluation


async def retrieve_evaluation_by_id(
    *, sqlmodel_session: Session, evaluation_id: int
) -> ApplicationEvaluation:
    statement: Any = select(ApplicationEvaluation).where(
        ApplicationEvaluation.id == evaluation_id
    )

    retrieved_evaluation = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_evaluation


async def update_evaluation(
    *,
    sqlmodel_session: Session,
    retrieved_evaluation: ApplicationEvaluation,
    evaluation: UpdateEvaluation,
) -> ApplicationEvaluation:
    retrieved_evaluation.sqlmodel_update(
        evaluation.model_dump(exclude_none=True, exclude_unset=True)
    )

    sqlmodel_session.add(retrieved_evaluation)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_evaluation)

    return retrieved_evaluation


async def upsert_evaluation(
    *, sqlmodel_session: Session, evaluation: Union[CreateEvaluation, UpdateEvaluation]
) -> ApplicationEvaluation:
    retrieved_evaluation = await retrieve_evaluation_by_id(
        sqlmodel_session=sqlmodel_session, evaluation_id=evaluation.id
    )
    if retrieved_evaluation:
        return await update_evaluation(
            sqlmodel_session=sqlmodel_session,
            retrieved_evaluation=retrieved_evaluation,
            evaluation=evaluation,
        )
    return await create_evaluation(
        sqlmodel_session=sqlmodel_session, evaluation=evaluation
    )


async def create(
    *, sqlmodel_session: Session, minio_client: Minio, application: CreateApplication
) -> Application:
    resume = None
    if getattr(application, "resume", None) is not None:
        resume = await create_resume(
            minio_client=minio_client,
            object_name=application.resume.name,
            data=BytesIO(application.resume.data),
            length=len(application.resume.data),
        )

    links = []
    if getattr(application, "links", None) is not None:
        links = [
            await upsert_link(sqlmodel_session=sqlmodel_session, link=link)
            for link in application.links
        ]

    evaluations = []
    if getattr(application, "evaluations", None) is not None:
        evaluations = [
            await upsert_evaluation(
                sqlmodel_session=sqlmodel_session, evaluation=evaluation
            )
            for evaluation in application.evaluations
        ]

    created_application = Application(
        **application.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"resume", "links", "evaluations"},
        ),
        resume=resume.object_name,
        links=links,
        evaluations=evaluations,
    )

    sqlmodel_session.add(created_application)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_application)

    return created_application


async def retrieve_by_id(
    *, sqlmodel_session: Session, application_id: int
) -> Application:
    statement: Any = select(Application).where(Application.id == application_id)

    retrieved_application: Application = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application


async def retrieve_by_email(*, sqlmodel_session: Session, email: str) -> Application:
    statement: Any = select(Application).where(Application.email == email)

    retrieved_application = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application


async def retrieve_by_phone(*, sqlmodel_session: Session, phone: str) -> Application:
    statement: Any = select(Application).where(Application.phone == phone)

    retrieved_application = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: ApplicationQueryParameters
) -> Sequence[Application]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Application, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        )
    }

    statement: Any = select(Application).offset(offset).limit(limit).where(*filters)

    retrieved_application = sqlmodel_session.exec(statement).all()

    return retrieved_application


async def update(
    *,
    sqlmodel_session: Session,
    retrieved_application: Application,
    application: UpdateApplication,
) -> Application:
    if getattr(application, "links", None) is not None:
        retrieved_application.links = [
            await upsert_link(sqlmodel_session=sqlmodel_session, link=link)
            for link in application.links
        ]

    if getattr(application, "evaluations", None) is not None:
        retrieved_application.evaluations = [
            await upsert_evaluation(
                sqlmodel_session=sqlmodel_session, evaluation=evaluation
            )
            for evaluation in application.evaluations
        ]

    retrieved_application.sqlmodel_update(
        application.model_dump(
            exclude_none=True, exclude_unset=True, exclude={"links", "evaluations"}
        )
    )

    sqlmodel_session.add(retrieved_application)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_application)

    return retrieved_application


async def delete(
    *, sqlmodel_session: Session, retrieved_application: Application
) -> Application:
    sqlmodel_session.delete(retrieved_application)
    sqlmodel_session.commit()

    return retrieved_application
