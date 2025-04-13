import uuid
from typing import List, Sequence
from sqlmodel import Session
from minio import Minio
from fastapi import Depends, APIRouter, Query
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.storage.service import get_minio_client
from src.talentgate.application import service as application_service
from src.talentgate.application.models import (
    Application,
    CreateApplication,
    ApplicationQueryParameters,
    UpdateApplication,
    CreatedApplication,
    RetrievedApplication,
    UpdatedApplication,
    DeletedApplication,
)
from src.talentgate.application.exceptions import (
    DuplicateEmailException,
    DuplicatePhoneException,
    ApplicationIdNotFoundException,
)

router = APIRouter(tags=["application"])


@router.post(
    path="/api/v1/applications",
    response_model=CreatedApplication,
    status_code=201,
)
async def create_application(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    minio_client: Minio = Depends(get_minio_client),
    application: CreateApplication,
) -> Application:
    retrieved_application = await application_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=application.email
    )

    if retrieved_application:
        raise DuplicateEmailException

    retrieved_application = await application_service.retrieve_by_phone(
        sqlmodel_session=sqlmodel_session, phone=application.phone
    )

    if retrieved_application:
        raise DuplicatePhoneException

    created_application = await application_service.create(
        sqlmodel_session=sqlmodel_session,
        minio_client=minio_client,
        application=application,
    )

    return created_application


@router.get(
    path="/api/v1/applications/{application_id}",
    response_model=RetrievedApplication,
    status_code=200,
)
async def retrieve_application(
    *,
    application_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    minio_client: Minio = Depends(get_minio_client),
) -> RetrievedApplication:
    retrieved_application = await application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, application_id=application_id
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    resume = await application_service.retrieve_resume(
        minio_client=minio_client, object_name=retrieved_application.resume
    )

    return RetrievedApplication(
        **retrieved_application.model_dump(exclude={"resume"}), resume=resume
    )


@router.get(
    path="/api/v1/applications",
    response_model=List[RetrievedApplication],
    status_code=200,
)
async def retrieve_applications(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: ApplicationQueryParameters = Query(),
) -> Sequence[Application]:
    retrieved_application = await application_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_application


@router.put(
    path="/api/v1/applications/{application_id}",
    response_model=UpdatedApplication,
    status_code=200,
)
async def update_application(
    *,
    application_id: int,
    application: UpdateApplication,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Application:
    retrieved_application = await application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, application_id=application_id
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    updated_application = await application_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_application=retrieved_application,
        application=application,
    )

    return updated_application


@router.delete(
    path="/api/v1/applications/{application_id}",
    response_model=DeletedApplication,
    status_code=200,
)
async def delete_application(
    *, application_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Application:
    retrieved_application = await application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, application_id=application_id
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    deleted_application = await application_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_application=retrieved_application
    )

    return deleted_application
