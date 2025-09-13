from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlmodel import Session

from config import Settings, get_settings
from src.talentgate.auth.exceptions import InvalidAuthorizationException
from src.talentgate.email.client import EmailClient, get_email_client
from src.talentgate.auth import service as auth_service
from src.talentgate.user import service as user_service
from src.talentgate.company import service as company_service
from src.talentgate.employee import service as employee_service
from src.talentgate.company.exceptions import CompanyIdNotFoundException
from src.talentgate.company.models import (
    Company,
    CompanyQueryParameters,
    CreateCompany,
    CreatedCompany,
    DeletedCompany,
    RetrievedCompany,
    UpdateCompany,
    UpdatedCompany,
)
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.employee.enums import EmployeeTitle
from src.talentgate.job.models import (
    Job,
    JobQueryParameters,
    RetrievedCompanyJob,
    RetrievedCompanyJobs,
    RetrievedJob,
)
from src.talentgate.user.models import (
    SubscriptionPlan,
    SubscriptionStatus,
    User,
    UserRole,
)
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["company"])


class CreateCompanyDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if (user.role == UserRole.ADMIN) or (
            user.subscription.plan == SubscriptionPlan.STANDARD
            and user.subscription.status == SubscriptionStatus.ACTIVE
        ):
            return True
        raise InvalidAuthorizationException


class RetrieveCompanyDependency:
    def __call__(
        self,
        company_id: int,
        user: User = Depends(retrieve_current_user),
    ) -> bool:
        if (user.role == UserRole.ADMIN) or (
            user.subscription.plan == SubscriptionPlan.STANDARD
            and user.employee.company.subscription.status == SubscriptionStatus.ACTIVE
            and user.employee.title in [EmployeeTitle.FOUNDER, EmployeeTitle.RECRUITER]
            and user.employee.company_id == company_id
        ):
            return True
        raise InvalidAuthorizationException


class RetrieveCompaniesDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class UpdateCompanyDependency:
    def __call__(
        self,
        company_id: int,
        user: User = Depends(retrieve_current_user),
    ) -> bool:
        if (user.role == UserRole.ADMIN) or (
            user.subscription.plan == SubscriptionPlan.STANDARD
            and user.employee.company.subscription.status == SubscriptionStatus.ACTIVE
            and user.employee.title in [EmployeeTitle.FOUNDER, EmployeeTitle.RECRUITER]
            and user.employee.company_id == company_id
        ):
            return True
        raise InvalidAuthorizationException


class DeleteCompanyDependency:
    def __call__(
        self,
        company_id: int,
        user: User = Depends(retrieve_current_user),
    ) -> bool:
        if (user.role == UserRole.ADMIN) or (
            user.subscription.plan == SubscriptionPlan.STANDARD
            and user.subscription.status == SubscriptionStatus.ACTIVE
            and user.employee.title == EmployeeTitle.FOUNDER
            and user.employee.company_id == company_id
        ):
            return True
        raise InvalidAuthorizationException


@router.get(
    path="/api/v1/careers/companies/{company_id}/jobs",
    response_model=list[RetrievedCompanyJobs],
    status_code=200,
)
async def retrieved_career_jobs(
    *,
    company_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    query_parameters: Annotated[JobQueryParameters, Query()],
) -> Sequence[Job]:
    return await company_service.retrieve_jobs_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
        company_id=company_id,
    )


@router.get(
    path="/api/v1/careers/companies/{company_id}/jobs/{job_id}",
    response_model=RetrievedCompanyJob,
    status_code=200,
)
async def retrieved_careers_job(
    *,
    company_id: int,
    job_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Job:
    return await company_service.retrieve_company_job(
        sqlmodel_session=sqlmodel_session,
        company_id=company_id,
        job_id=job_id,
    )


@router.get(
    path="/api/v1/companies/{company_id}/jobs",
    response_model=list[RetrievedJob],
    status_code=200,
)
async def retrieved_company_jobs(
    *,
    company_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    query_parameters: Annotated[JobQueryParameters, Query()],
) -> Sequence[Job]:
    return await company_service.retrieve_jobs_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
        company_id=company_id,
    )


@router.post(
    path="/api/v1/companies",
    response_model=CreatedCompany,
    status_code=201,
    dependencies=[Depends(CreateCompanyDependency())],
)
async def create_company(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    company: CreateCompany,
) -> Company:
    return await company_service.create(
        sqlmodel_session=sqlmodel_session,
        company=company,
    )


@router.get(
    path="/api/v1/companies/{company_id}",
    response_model=RetrievedCompany,
    status_code=200,
    dependencies=[Depends(RetrieveCompanyDependency())],
)
async def retrieve_company(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    company_id: int,
) -> Company:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        company_id=company_id,
    )

    if not retrieved_company:
        raise CompanyIdNotFoundException

    return retrieved_company


@router.get(
    path="/api/v1/companies",
    response_model=list[RetrievedCompany],
    status_code=200,
    dependencies=[Depends(RetrieveCompaniesDependency())],
)
async def retrieve_companies(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    query_parameters: Annotated[CompanyQueryParameters, Query()],
) -> Sequence[Company]:
    return await company_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
    )


@router.put(
    path="/api/v1/companies/{company_id}",
    response_model=UpdatedCompany,
    status_code=200,
    dependencies=[Depends(UpdateCompanyDependency())],
)
async def update_company(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    email_client: Annotated[EmailClient, Depends(get_email_client)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
    company_id: int,
    company: UpdateCompany,
) -> Company:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        company_id=company_id,
    )

    if not retrieved_company:
        raise CompanyIdNotFoundException

    updated_company = await company_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=retrieved_company,
        company=company,
    )

    for employee in company.employees:
        if not employee.user.id:
            retrieved_user = await user_service.retrieve_by_email(
                sqlmodel_session=sqlmodel_session, email=employee.user.email
            )

            token = auth_service.encode_token(
                user_id=str(employee.user.id),
                key=settings.access_token_key,
                seconds=settings.access_token_expiration,
            )

            context = {
                "username": employee.user.username,
                "link": f"${settings.frontend_base_url}/verify?token={token}",
            }

            await company_service.send_onboarding_email(
                email_client=email_client,
                background_tasks=background_tasks,
                context=context,
                from_addr=settings.smtp_email,
                to_addrs=retrieved_user.email,
            )

    return updated_company


@router.delete(
    path="/api/v1/companies/{company_id}",
    response_model=DeletedCompany,
    status_code=200,
    dependencies=[Depends(DeleteCompanyDependency())],
)
async def delete_company(
    *,
    company_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Company:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        company_id=company_id,
    )

    if not retrieved_company:
        raise CompanyIdNotFoundException

    return await company_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=retrieved_company,
    )
