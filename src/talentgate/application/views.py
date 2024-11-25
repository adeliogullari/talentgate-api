from typing import List, Sequence
from sqlmodel import Session
from fastapi import Depends, APIRouter, Query
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.application import service as application_service
from src.talentgate.application.models import (
    Application,
    CreateApplication,
    ApplicationQueryParameters,
    UpdateApplication,
    ApplicationEvaluation,
    ApplicationEvaluationRequest,
)
from src.talentgate.application.exceptions import (
    DuplicateEmailException,
    DuplicateEvaluationException,
    DuplicatePhoneException,
    ApplicationIdNotFoundException,
    EvaluationIdNotFoundException,
)

router = APIRouter(tags=["application"])


# Evaluation Endpoints
@router.post(
    path="/api/v1/applications/evaluations",
    response_model=ApplicationEvaluation,
    status_code=201,
)
async def create_application_evaluation(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    application_evaluation: ApplicationEvaluationRequest,
) -> ApplicationEvaluation:
    retrieved_application_evaluation = await application_service.retrieve_application_evaluation_by_employee_and_application(
        sqlmodel_session=sqlmodel_session,
        employee_id=application_evaluation.employee_id,
        application_id=application_evaluation.application_id,
    )

    if retrieved_application_evaluation:
        raise DuplicateEvaluationException

    created_application_evaluation = (
        await application_service.create_application_evaluation(
            sqlmodel_session=sqlmodel_session,
            application_evaluation=application_evaluation,
        )
    )

    return created_application_evaluation


@router.get(
    path="/api/v1/applications/evaluations/{evaluation_id}",
    response_model=ApplicationEvaluation,
    status_code=200,
)
async def retrieve_application_evaluation(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    evaluation_id: int,
) -> ApplicationEvaluation:
    retrieved_application_evaluation = (
        await application_service.retrieve_application_evaluation_by_id(
            sqlmodel_session=sqlmodel_session, application_evaluation_id=evaluation_id
        )
    )

    if not retrieved_application_evaluation:
        raise EvaluationIdNotFoundException

    return retrieved_application_evaluation


@router.get(
    path="/api/v1/applications/{application_id}/evaluations",
    response_model=List[ApplicationEvaluation],
    status_code=200,
)
async def retrieve_application_evaluations_by_application(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    application_id: int,
) -> List[ApplicationEvaluation]:
    retrieved_application_evaluations = (
        await application_service.retrieve_application_evaluations_by_application(
            sqlmodel_session=sqlmodel_session, application_id=application_id
        )
    )

    if not retrieved_application_evaluations:
        raise ApplicationIdNotFoundException

    return retrieved_application_evaluations


@router.put(
    path="/api/v1/applications/evaluations/{evaluation_id}",
    response_model=ApplicationEvaluation,
    status_code=200,
)
async def update_application_evaluation(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    evaluation_id: int,
    application_evaluation: ApplicationEvaluationRequest,
) -> ApplicationEvaluation:
    retrieved_application_evaluation = (
        await application_service.retrieve_application_evaluation_by_id(
            sqlmodel_session=sqlmodel_session, application_evaluation_id=evaluation_id
        )
    )

    if not retrieved_application_evaluation:
        raise EvaluationIdNotFoundException

    updated_application_evaluation = (
        await application_service.update_application_evaluation(
            sqlmodel_session=sqlmodel_session,
            retrieved_application_evaluation=retrieved_application_evaluation,
            application_evaluation=application_evaluation,
        )
    )

    return updated_application_evaluation


@router.delete(
    path="/api/v1/applications/evaluations/{evaluation_id}",
    response_model=ApplicationEvaluation,
    status_code=200,
)
async def delete_application_evaluation(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    evaluation_id: int,
) -> ApplicationEvaluation:
    retrieved_application_evaluation = (
        await application_service.retrieve_application_evaluation_by_id(
            sqlmodel_session=sqlmodel_session, application_evaluation_id=evaluation_id
        )
    )

    if not retrieved_application_evaluation:
        raise EvaluationIdNotFoundException

    deleted_application_evaluation = (
        await application_service.delete_application_evaluation(
            sqlmodel_session=sqlmodel_session,
            retrieved_application_evaluation=retrieved_application_evaluation,
        )
    )

    return deleted_application_evaluation


# Application Endpoints
@router.post(
    path="/api/v1/applications",
    response_model=Application,
    status_code=201,
)
async def create_application(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    application: CreateApplication,
) -> Application:
    retrieved_application = await application_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, application_email=application.email
    )

    if retrieved_application:
        raise DuplicateEmailException

    retrieved_application = await application_service.retrieve_by_phone(
        sqlmodel_session=sqlmodel_session, application_phone=application.phone
    )

    if retrieved_application:
        raise DuplicatePhoneException

    created_application = await application_service.create(
        sqlmodel_session=sqlmodel_session, application=application
    )

    return created_application


@router.get(
    path="/api/v1/applications/{application_id}",
    response_model=Application,
    status_code=200,
)
async def retrieve_application(
    *, application_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Application:
    retrieved_application = await application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, application_id=application_id
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    return retrieved_application


@router.get(
    path="/api/v1/applications",
    response_model=List[Application],
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
    response_model=Application,
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
    response_model=Application,
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
