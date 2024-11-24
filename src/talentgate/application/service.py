from typing import Any, Sequence, List
from sqlmodel import select, Session
from src.talentgate.application.models import (
    Application,
    ApplicationQueryParameters, CreateApplication, UpdateApplication, ApplicationEvaluationRequest,
    ApplicationEvaluation,
)


# APPLICATION EVALUATION SERVICES
async def create_application_evaluation(*, sqlmodel_session: Session, application_evaluation: ApplicationEvaluationRequest) -> ApplicationEvaluation:
    created_application_evaluation = ApplicationEvaluation(
        **application_evaluation.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_application_evaluation)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_application_evaluation)

    return created_application_evaluation


async def retrieve_application_evaluation_by_employee_and_application(
    *, sqlmodel_session: Session, employee_id: int, application_id: int
) -> ApplicationEvaluation:
    statement: Any = select(ApplicationEvaluation).where(
        (ApplicationEvaluation.employee_id == employee_id) &
        (ApplicationEvaluation.application_id == application_id)
    )
    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_application_evaluation_by_id(*, sqlmodel_session: Session, application_evaluation_id: int) -> ApplicationEvaluation:
    statement: Any = select(ApplicationEvaluation).where(ApplicationEvaluation.id == application_evaluation_id)

    retrieved_application_evaluation = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application_evaluation


async def retrieve_application_evaluations_by_application(*, sqlmodel_session: Session, application_id: int) -> List[ApplicationEvaluation]:
    retrieved_application = await retrieve_by_id(sqlmodel_session=sqlmodel_session, application_id=application_id)
    retrieved_application_evaluations = retrieved_application.evaluations

    return retrieved_application_evaluations


async def update_application_evaluation(
    *, sqlmodel_session: Session, retrieved_application_evaluation: ApplicationEvaluation, application_evaluation: ApplicationEvaluationRequest
) -> ApplicationEvaluation:
    retrieved_application_evaluation.sqlmodel_update(application_evaluation)

    sqlmodel_session.add(retrieved_application_evaluation)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_application_evaluation)

    return retrieved_application_evaluation


async def delete_application_evaluation(
    *, sqlmodel_session: Session, retrieved_application_evaluation: ApplicationEvaluation
) -> ApplicationEvaluation:
    sqlmodel_session.delete(retrieved_application_evaluation)
    sqlmodel_session.commit()

    return retrieved_application_evaluation


# APPLICATION SERVICES
async def create(*, sqlmodel_session: Session, application: CreateApplication) -> Application:
    created_application = Application(
        **application.model_dump(exclude_unset=True, exclude_none=True),
    )

    sqlmodel_session.add(created_application)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_application)

    return created_application


async def retrieve_by_id(*, sqlmodel_session: Session, application_id: int) -> Application:
    statement: Any = select(Application).where(Application.id == application_id)

    retrieved_application = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application


async def retrieve_by_firstname(
    *, sqlmodel_session: Session, application_firstname: str
) -> Application:
    statement: Any = select(Application).where(Application.firstname == application_firstname)

    retrieved_application = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application


async def retrieve_by_lastname(
    *, sqlmodel_session: Session, application_lastname: str
) -> Application:
    statement: Any = select(Application).where(Application.lastname == application_lastname)

    retrieved_application = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application


async def retrieve_by_email(
    *, sqlmodel_session: Session, application_email: str
) -> Application:
    statement: Any = select(Application).where(Application.email == application_email)

    retrieved_application = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_application


async def retrieve_by_phone(
    *, sqlmodel_session: Session, application_phone: str
) -> Application:
    statement: Any = select(Application).where(Application.phone == application_phone)

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
    *, sqlmodel_session: Session, retrieved_application: Application, application: UpdateApplication
) -> Application:
    retrieved_application.sqlmodel_update(application)

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

