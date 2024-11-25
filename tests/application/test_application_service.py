from datetime import datetime

from sqlmodel import Session
from src.talentgate.application.models import (
    Application,
    ApplicationEvaluation,
    ApplicationEvaluationRequest,
    CreateApplication,
    UpdateApplication,
)
from src.talentgate.application.service import (
    create,
    create_application_evaluation,
    retrieve_application_evaluation_by_id,
    retrieve_application_evaluation_by_employee_and_application,
    retrieve_application_evaluations_by_application,
    retrieve_by_id,
    retrieve_by_firstname,
    retrieve_by_lastname,
    retrieve_by_email,
    retrieve_by_phone,
    update,
    delete,
    update_application_evaluation,
    delete_application_evaluation,
)
from src.talentgate.employee.models import Employee
from tests.application.conftest import make_application_evaluation


async def test_create_application_evaluation(
    sqlmodel_session: Session, application: Application, employee: Employee
) -> None:
    evaluation = ApplicationEvaluationRequest(
        comment="comment",
        rating=5,
        application_id=application.id,
        employee_id=employee.id,
    )

    created_evaluation = await create_application_evaluation(
        sqlmodel_session=sqlmodel_session, application_evaluation=evaluation
    )

    assert created_evaluation.comment == evaluation.comment
    assert created_evaluation.application.id == application.id
    assert created_evaluation.employee.id == employee.id


async def test_retrieve_application_evaluation_by_employee_and_application(
    sqlmodel_session: Session,
    application: Application,
    employee: Employee,
    application_evaluation: ApplicationEvaluation,
) -> None:
    retrieved_application_evaluation = (
        await retrieve_application_evaluation_by_employee_and_application(
            sqlmodel_session=sqlmodel_session,
            employee_id=employee.id,
            application_id=application.id,
        )
    )

    assert retrieved_application_evaluation.comment == application_evaluation.comment
    assert retrieved_application_evaluation.application.id == application.id
    assert retrieved_application_evaluation.employee.id == employee.id


async def test_retrieve_application_evaluation_by_id(
    sqlmodel_session: Session, application_evaluation: ApplicationEvaluation
) -> None:
    retrieved_application_evaluation = await retrieve_application_evaluation_by_id(
        sqlmodel_session=sqlmodel_session,
        application_evaluation_id=application_evaluation.id,
    )

    assert retrieved_application_evaluation.comment == application_evaluation.comment


async def test_retrieve_application_evaluations(
    sqlmodel_session: Session, application: Application
) -> None:
    retrieved_application_evaluations = (
        await retrieve_application_evaluations_by_application(
            sqlmodel_session=sqlmodel_session, application_id=application.id
        )
    )

    assert retrieved_application_evaluations == application.evaluations


async def test_update_application_evaluation(
    sqlmodel_session: Session, make_application_evaluation
) -> None:
    retrieved_application_evaluation = make_application_evaluation()

    application_evaluation = ApplicationEvaluationRequest(
        comment="updated_comment", rating="1"
    )

    updated_application_evaluation = await update_application_evaluation(
        sqlmodel_session=sqlmodel_session,
        retrieved_application_evaluation=retrieved_application_evaluation,
        application_evaluation=application_evaluation,
    )

    assert application_evaluation.comment == updated_application_evaluation.comment


async def test_delete_application_evaluation(
    sqlmodel_session: Session, make_application_evaluation
) -> None:
    retrieved_application_evaluation = make_application_evaluation()

    deleted_application_evaluation = await delete_application_evaluation(
        sqlmodel_session=sqlmodel_session,
        retrieved_application_evaluation=retrieved_application_evaluation,
    )

    assert (
        retrieved_application_evaluation.comment
        == deleted_application_evaluation.comment
    )


async def test_create(sqlmodel_session: Session) -> None:
    application = CreateApplication(
        firstname="firstname",
        lastname="lastname",
        email="email@gmail.com",
        phone="534654325",
        city="test_city",
        state="test_state",
        country="test_country",
        postal_code="32214",
        resume="cv/test.pdf",
        earliest_start_date=datetime.now(),
    )

    created_application = await create(
        sqlmodel_session=sqlmodel_session, application=application
    )

    assert created_application.email == application.email


async def test_retrieve_by_id(
    sqlmodel_session: Session, application: Application
) -> None:
    retrieved_application = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, application_id=application.id
    )

    assert retrieved_application.id == application.id


async def test_retrieve_by_firstname(
    sqlmodel_session: Session, application: Application
) -> None:
    retrieved_application = await retrieve_by_firstname(
        sqlmodel_session=sqlmodel_session, application_firstname=application.firstname
    )

    assert retrieved_application.firstname == application.firstname


async def test_retrieve_by_lastname(
    sqlmodel_session: Session, application: Application
) -> None:
    retrieved_application = await retrieve_by_lastname(
        sqlmodel_session=sqlmodel_session, application_lastname=application.lastname
    )

    assert retrieved_application.lastname == application.lastname


async def test_retrieve_by_email(
    sqlmodel_session: Session, application: Application
) -> None:
    retrieved_application = await retrieve_by_email(
        sqlmodel_session=sqlmodel_session, application_email=application.email
    )

    assert retrieved_application.email == application.email


async def test_retrieve_by_phone(
    sqlmodel_session: Session, application: Application
) -> None:
    retrieved_application = await retrieve_by_phone(
        sqlmodel_session=sqlmodel_session, application_phone=application.phone
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
        sqlmodel_session=sqlmodel_session, retrieved_application=retrieved_application
    )

    assert retrieved_application.firstname == deleted_application.firstname
