from datetime import datetime
from sqlmodel import Session
from src.talentgate.applicant.models import (
    Applicant,
    CreateApplicant,
    UpdateApplicant,
)
from src.talentgate.applicant.service import (
    create,
    retrieve_by_id,
    retrieve_by_firstname,
    retrieve_by_lastname,
    retrieve_by_email,
    retrieve_by_phone,
    update,
    delete,
)


async def test_create(sqlmodel_session: Session) -> None:
    applicant = CreateApplicant(
        firstname="firstname",
        lastname="lastname",
        email="email@gmail.com",
        phone="534654325",
        address="addr",
        city="test_city",
        state="test_state",
        country="test_country",
        postal_code="32214",
        linkedin_url="www.linkedin.com/in/test",
        cv_url="cv/test.pdf",
        earliest_start_date=datetime.now(),
    )

    created_applicant = await create(
        sqlmodel_session=sqlmodel_session, applicant=applicant
    )

    assert created_applicant.email == applicant.email


async def test_retrieve_by_id(sqlmodel_session: Session, applicant: Applicant) -> None:
    retrieved_applicant = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, applicant_id=applicant.id
    )

    assert retrieved_applicant.id == applicant.id


async def test_retrieve_by_firstname(
    sqlmodel_session: Session, applicant: Applicant
) -> None:
    retrieved_applicant = await retrieve_by_firstname(
        sqlmodel_session=sqlmodel_session, applicant_firstname=applicant.firstname
    )

    assert retrieved_applicant.firstname == applicant.firstname


async def test_retrieve_by_lastname(
    sqlmodel_session: Session, applicant: Applicant
) -> None:
    retrieved_applicant = await retrieve_by_lastname(
        sqlmodel_session=sqlmodel_session, applicant_lastname=applicant.lastname
    )

    assert retrieved_applicant.lastname == applicant.lastname


async def test_retrieve_by_email(
    sqlmodel_session: Session, applicant: Applicant
) -> None:
    retrieved_applicant = await retrieve_by_email(
        sqlmodel_session=sqlmodel_session, applicant_email=applicant.email
    )

    assert retrieved_applicant.email == applicant.email


async def test_retrieve_by_phone(
    sqlmodel_session: Session, applicant: Applicant
) -> None:
    retrieved_applicant = await retrieve_by_phone(
        sqlmodel_session=sqlmodel_session, applicant_phone=applicant.phone
    )

    assert retrieved_applicant.phone == applicant.phone


async def test_update(sqlmodel_session: Session, make_applicant) -> None:
    retrieved_applicant = make_applicant()

    applicant = UpdateApplicant(
        firstname="updatedfirstname",
        lastname="updatedlastname",
        email="updatedemail@gmail.com",
        phone="updated534654325",
        address="updatedaddr",
        city="updatedtest_city",
        state="updatedtest_state",
        country="updatedtest_country",
        postal_code="32214",
        linkedin_url="www.linkedin.com/in/test",
        cv_url="cv/test.pdf",
        earliest_start_date=datetime.now(),
    )

    updated_applicant = await update(
        sqlmodel_session=sqlmodel_session,
        retrieved_applicant=retrieved_applicant,
        applicant=applicant,
    )

    assert applicant.firstname == updated_applicant.firstname


async def test_delete(sqlmodel_session, make_applicant) -> None:
    retrieved_applicant = make_applicant()

    deleted_applicant = await delete(
        sqlmodel_session=sqlmodel_session, retrieved_applicant=retrieved_applicant
    )

    assert retrieved_applicant.firstname == deleted_applicant.firstname
