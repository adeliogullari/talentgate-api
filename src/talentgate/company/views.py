from sqlmodel import Session
from typing import List, Sequence
from fastapi import Depends, APIRouter, Query
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.company import service as company_service
from src.talentgate.company.models import (
    Company,
    CreateCompany,
    CreatedCompany,
    RetrievedCompany,
    CompanyQueryParameters,
    UpdateCompany,
    UpdatedCompany,
    DeletedCompany,
)
from src.talentgate.company.exceptions import (
    IdNotFoundException,
    DuplicateUsernameException,
    DuplicateEmailException,
)

router = APIRouter(tags=["company"])


@router.post(
    path="/api/v1/companies",
    response_model=CreatedCompany,
    status_code=201,
)
async def create_company(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    company: CreateCompany,
) -> Company:
    created_company = await company_service.create(
        sqlmodel_session=sqlmodel_session, company=company
    )

    return created_company


@router.get(
    path="/api/v1/companies/{company_id}",
    response_model=RetrievedCompany,
    status_code=200,
)
async def retrieve_company(
    *, sqlmodel_session: Session = Depends(get_sqlmodel_session), company_id: int
) -> Company:
    retrieved_employee = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=company_id
    )

    return retrieved_employee


@router.get(
    path="/api/v1/companies",
    response_model=List[RetrievedCompany],
    status_code=200,
)
async def retrieve_companies(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: CompanyQueryParameters = Query(),
) -> Sequence[Company]:
    retrieved_user = await company_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_user


@router.put(
    path="/api/v1/companies/{company_id}",
    response_model=UpdatedCompany,
    status_code=200,
)
async def update_company(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    company_id: int,
    company: UpdateCompany,
) -> Company:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=company_id
    )

    if not retrieved_company:
        raise IdNotFoundException

    updated_user = await company_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=retrieved_company,
        company=company,
    )

    return updated_user


@router.delete(
    path="/api/v1/companies/{company_id}",
    response_model=DeletedCompany,
    status_code=200,
)
async def delete_company(
    *, company_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Company:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=company_id
    )

    if not retrieved_company:
        raise IdNotFoundException

    deleted_user = await company_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_company=retrieved_company
    )

    return deleted_user
