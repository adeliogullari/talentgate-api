from typing import Any, Sequence
from sqlmodel import select, Session
from src.talentgate.company.models import (
    Company,
    CreateCompany,
    CompanyQueryParameters,
    UpdateCompany,
)
from config import get_settings

settings = get_settings()


async def create(*, sqlmodel_session: Session, company: CreateCompany) -> Company:
    created_company = Company(
        **company.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_company)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_company)

    return created_company


async def retrieve_by_id(*, sqlmodel_session: Session, company_id: int) -> Company:
    statement: Any = select(Company).where(Company.id == company_id)

    retrieved_user = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_user


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: CompanyQueryParameters
) -> Sequence[Company]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = {
        getattr(Company, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        )
    }

    statement: Any = select(Company).offset(offset).limit(limit).where(*filters)

    retrieved_user = sqlmodel_session.exec(statement).all()

    return retrieved_user


async def update(
    *, sqlmodel_session: Session, retrieved_company: Company, company: UpdateCompany
) -> Company:
    retrieved_company.sqlmodel_update(company)

    sqlmodel_session.add(retrieved_company)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_company)

    return retrieved_company


async def delete(*, sqlmodel_session: Session, retrieved_company: Company) -> Company:
    sqlmodel_session.delete(retrieved_company)
    sqlmodel_session.commit()

    return retrieved_company
