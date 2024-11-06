from typing import List, Sequence
from sqlmodel import Session
from fastapi import Depends, APIRouter, Query
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.applicant import service as applicant_service
from src.talentgate.applicant.models import (
    Applicant,
    ApplicantQueryParameters
)
from src.talentgate.applicant.exceptions import (
    DuplicateEmailException,
    DuplicatePhoneException,
    IdNotFoundException,
)
from src.talentgate.auth.crypto.token import BearerToken
from config import Settings, get_settings

router = APIRouter(tags=["applicant"])

@router.post(
    path="/api/v1/applicant",
    response_model=Applicant,
    status_code=201,
)
async def create_applicant(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    applicant: Applicant,
) -> Applicant:
    retrieved_applicant = await applicant_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, applicant_email=applicant.email
    )

    if retrieved_applicant:
        raise DuplicateEmailException

    retrieved_applicant = await applicant_service.retrieve_by_phone(
        sqlmodel_session=sqlmodel_session, applicant_phone=applicant.phone
    )

    if retrieved_applicant:
        raise DuplicatePhoneException

    created_applicant = await applicant_service.create(
        sqlmodel_session=sqlmodel_session, applicant=applicant
    )

    return created_applicant


@router.get(
    path="/api/v1/applicant/{applicant_id}",
    response_model=Applicant,
    status_code=200,
)
async def retrieve_applicant(
    *, applicant_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Applicant:
    retrieved_applicant = await applicant_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, applicant_id=applicant_id
    )

    if not retrieved_applicant:
        raise IdNotFoundException

    return retrieved_applicant


@router.get(
    path="/api/v1/applicant",
    response_model=List[Applicant],
    status_code=200,
)
async def retrieve_applicants(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: ApplicantQueryParameters = Query(),
) -> Sequence[Applicant]:
    retrieved_applicant = await applicant_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_applicant


@router.put(
    path="/api/v1/applicant/{applicant_id}",
    response_model=Applicant,
    status_code=200,
)
async def update_applicant(
    *,
    applicant_id: int,
    applicant: Applicant,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Applicant:
    retrieved_applicant = await applicant_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, applicant_id=applicant_id
    )

    if not retrieved_applicant:
        raise IdNotFoundException

    updated_applicant = await applicant_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_applicant=retrieved_applicant, applicant=applicant
    )

    return updated_applicant


@router.delete(
    path="/api/v1/applicant/{applicant_id}",
    response_model=Applicant,
    status_code=200,
)
async def delete_applicant(
    *, applicant_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Applicant:
    retrieved_applicant = await applicant_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, applicant_id=applicant_id
    )

    if not retrieved_applicant:
        raise IdNotFoundException

    deleted_applicant = await applicant_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_applicant=retrieved_applicant
    )

    return deleted_applicant
