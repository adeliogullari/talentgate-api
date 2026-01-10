from collections.abc import Sequence
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from minio import Minio
from sqlmodel import Session, select

from src.talentgate.application import service as application_service
from src.talentgate.application.exceptions import (
    ApplicationIdNotFoundException,
    DuplicateEmailException,
    DuplicatePhoneException,
)
from src.talentgate.application.models import (
    Application,
    ApplicationQueryParameters,
    CreateApplication,
    CreatedApplication,
    DeletedApplication,
    RetrievedApplication,
    UpdateApplication,
    UpdatedApplication,
)
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.storage.service import get_minio_client

router = APIRouter(tags=["application"])


@router.post(
    path="/api/v1/applications",
    response_model=CreatedApplication,
    status_code=201,
)
async def create_application(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    application: CreateApplication,
) -> Application:
    retrieved_application = await application_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=application.email,
    )

    if retrieved_application:
        raise DuplicateEmailException

    retrieved_application = await application_service.retrieve_by_phone(
        sqlmodel_session=sqlmodel_session,
        phone=application.phone,
    )

    if retrieved_application:
        raise DuplicatePhoneException

    return await application_service.create(
        sqlmodel_session=sqlmodel_session,
        application=application,
    )


@router.get(
    path="/api/v1/applications/{application_id}",
    status_code=200,
)
async def retrieve_application(
    *,
    application_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    minio_client: Annotated[Minio, Depends(get_minio_client)],
) -> RetrievedApplication:
    retrieved_application = await application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        application_id=application_id,
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    resume = await application_service.retrieve_resume(
        minio_client=minio_client,
        object_name=retrieved_application.resume,
    )

    return RetrievedApplication(
        **retrieved_application.model_dump(exclude={"resume"}),
        resume=resume,
    )


@router.get(
    path="/api/v1/applications",
    response_model=list[RetrievedApplication],
    status_code=200,
)
async def retrieve_applications(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    minio_client: Annotated[Minio, Depends(get_minio_client)],
    query_parameters: Annotated[ApplicationQueryParameters, Query()],
) -> Sequence[RetrievedApplication]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = [
        getattr(Application, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"},
            exclude_unset=True,
            exclude_none=True,
        ).items()
    ]

    statement: Any = select(Application).offset(offset).limit(limit).where(*filters)

    retrieved_applications = []
    for retrieved_application in sqlmodel_session.exec(statement).all():
        resume = await application_service.retrieve_resume(
            minio_client=minio_client,
            object_name=retrieved_application.resume,
        )
        retrieved_applications.append(
            RetrievedApplication(
                **retrieved_application.model_dump(exclude={"resume"}),
                resume=resume,
            ),
        )

    return retrieved_applications


@router.put(
    path="/api/v1/applications/{application_id}",
    response_model=UpdatedApplication,
    status_code=200,
)
async def update_application(
    *,
    application_id: int,
    application: UpdateApplication,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Application:
    retrieved_application = await application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        application_id=application_id,
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    return await application_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_application=retrieved_application,
        application=application,
    )


@router.delete(
    path="/api/v1/applications/{application_id}",
    response_model=DeletedApplication,
    status_code=200,
)
async def delete_application(
    *,
    application_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Application:
    retrieved_application = await application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        application_id=application_id,
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    return await application_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_application=retrieved_application,
    )
