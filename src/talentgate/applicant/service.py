from typing import Any, Sequence
from sqlmodel import select, Session
from src.talentgate.applicant.models import (
    Applicant,
    ApplicantQueryParameters, CreateApplicant, UpdateApplicant,
)


async def create(*, sqlmodel_session: Session, applicant: CreateApplicant) -> Applicant:
    created_applicant = Applicant(
        **applicant.model_dump(exclude_unset=True, exclude_none=True),
    )

    sqlmodel_session.add(created_applicant)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_applicant)

    return created_applicant


async def retrieve_by_id(*, sqlmodel_session: Session, applicant_id: int) -> Applicant:
    statement: Any = select(Applicant).where(Applicant.id == applicant_id)

    retrieved_applicant = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_applicant


async def retrieve_by_firstname(
    *, sqlmodel_session: Session, applicant_firstname: str
) -> Applicant:
    statement: Any = select(Applicant).where(Applicant.firstname == applicant_firstname)

    retrieved_applicant = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_applicant


async def retrieve_by_lastname(
    *, sqlmodel_session: Session, applicant_lastname: str
) -> Applicant:
    statement: Any = select(Applicant).where(Applicant.lastname == applicant_lastname)

    retrieved_applicant = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_applicant


async def retrieve_by_email(
    *, sqlmodel_session: Session, applicant_email: str
) -> Applicant:
    statement: Any = select(Applicant).where(Applicant.email == applicant_email)

    retrieved_applicant = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_applicant


async def retrieve_by_phone(
    *, sqlmodel_session: Session, applicant_phone: str
) -> Applicant:
    statement: Any = select(Applicant).where(Applicant.phone == applicant_phone)

    retrieved_applicant = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_applicant


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: ApplicantQueryParameters
) -> Sequence[Applicant]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Applicant, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        )
    }

    statement: Any = select(Applicant).offset(offset).limit(limit).where(*filters)

    retrieved_applicant = sqlmodel_session.exec(statement).all()

    return retrieved_applicant


async def update(
    *, sqlmodel_session: Session, retrieved_applicant: Applicant, applicant: UpdateApplicant
) -> Applicant:
    retrieved_applicant.sqlmodel_update(applicant)

    sqlmodel_session.add(retrieved_applicant)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_applicant)

    return retrieved_applicant


async def delete(
    *, sqlmodel_session: Session, retrieved_applicant: Applicant
) -> Applicant:
    sqlmodel_session.delete(retrieved_applicant)
    sqlmodel_session.commit()

    return retrieved_applicant
