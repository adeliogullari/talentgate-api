from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

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
) -> Application:
    retrieved_application = await application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        application_id=application_id,
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    return retrieved_application


@router.get(
    path="/api/v1/applications",
    response_model=list[RetrievedApplication],
    status_code=200,
)
async def retrieve_applications(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    query_parameters: Annotated[ApplicationQueryParameters, Query()],
) -> Sequence[Application]:
    return await application_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
    )


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
