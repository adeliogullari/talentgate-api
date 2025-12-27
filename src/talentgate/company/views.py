import random
import string
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from io import BytesIO
from typing import Annotated, Sequence
from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Query,
    UploadFile,
)
from minio import Minio
from sqlmodel import Session
from starlette.responses import JSONResponse, StreamingResponse

from config import Settings, get_settings
from src.talentgate.auth import service as auth_service
from src.talentgate.auth.exceptions import (
    InvalidAuthorizationException,
    InvalidOneTimeTokenException,
)
from src.talentgate.auth.models import AuthenticationTokens
from src.talentgate.company import service as company_service
from src.talentgate.company.exceptions import (
    CompanyIdNotFoundException,
)
from src.talentgate.company.models import (
    Company,
    CompanyEmployee,
    CompanyLink,
    CompanyLocation,
    CompanyQueryParameters,
    CreateCompany,
    CreatedCompany,
    DeletedCompany,
    DeletedCurrentCompany,
    EmployeeInvitation,
    InvitationAcceptance,
    RetrievedCompany,
    RetrievedCurrentCompany,
    RetrievedCurrentCompanyJob,
    UpdateCompany,
    UpdateCurrentCompany,
    UpdatedCompany,
)
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.email.client import EmailClient, get_email_client
from src.talentgate.employee import service as employee_service
from src.talentgate.employee.enums import EmployeeTitle
from src.talentgate.employee.exceptions import EmployeeIdNotFoundException
from src.talentgate.employee.models import CreateEmployee, DeletedEmployee, Employee, UpdateEmployee, \
    EmployeeQueryParameters
from src.talentgate.job.models import (
    Job,
    JobQueryParameters,
    RetrievedCompanyJob,
    RetrievedCompanyJobs,
    RetrievedJob,
)
from src.talentgate.storage.service import get_minio_client
from src.talentgate.user import service as user_service
from src.talentgate.user.models import (
    CreateSubscription,
    CreateUser,
    SubscriptionPlan,
    SubscriptionStatus,
    User,
    UserRole,
)
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["company"])


@router.get(
    path="/api/v1/me/company",
    response_model=RetrievedCurrentCompany,
    status_code=200,
)
async def retrieve_current_company(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
) -> Company:
    return await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=retrieved_user.employee.company_id
    )


@router.get(
    path="/api/v1/me/company/employees",
    response_model=list[CompanyEmployee],
    status_code=200,
)
async def retrieve_current_company_employees(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_company: Annotated[User, Depends(retrieve_current_company)],
    query_parameters: Annotated[EmployeeQueryParameters, Query()],
) -> Sequence[Employee]:
    return await employee_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, company_id=retrieved_company.id, query_parameters=query_parameters
    )


@router.put(
    path="/api/v1/me/company/employees/{employee_id}",
    response_model=list[CompanyEmployee],
    status_code=200,
)
async def update_current_company_employee(
    *,
    employee_id: int,
    employee: UpdateEmployee,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_company: Annotated[User, Depends(retrieve_current_company)],
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        company_id=retrieved_company.id,
        employee_id=employee_id,
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    return await employee_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=retrieved_employee,
        employee=employee,
    )


@router.delete(
    path="/api/v1/me/company/employees/{employee_id}",
    response_model=DeletedEmployee,
    status_code=200,
)
async def delete_current_company_employee(
    *,
    employee_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_company: Annotated[User, Depends(retrieve_current_company)],
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        company_id=retrieved_company.id,
        employee_id=employee_id,
    )

    if not retrieved_employee:
        raise EmployeeIdNotFoundException

    return await employee_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=retrieved_employee,
    )


@router.get(
    path="/api/v1/me/company/jobs",
    response_model=list[RetrievedCurrentCompanyJob],
    status_code=200,
)
async def retrieve_current_company_jobs(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
) -> list[Job]:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=retrieved_user.employee.company_id
    )

    return retrieved_company.jobs


@router.get(
    path="/api/v1/me/company/jobs/{job_id}/applications",
    response_model=list[RetrievedCurrentCompanyJob],
    status_code=200,
)
async def retrieve_current_company_job_applications(
    *,
    job_id: str,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
) -> list[Job]:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=retrieved_user.employee.company_id
    )

    job = next(filter(lambda job: job.id == job_id, retrieved_company.jobs))

    return job.applications


@router.get(
    path="/api/v1/me/company/logo",
    response_model=None,
    status_code=200,
)
async def retrieve_current_company_logo(
    *,
    minio_client: Annotated[Minio, Depends(get_minio_client)],
    retrieved_company: Annotated[Company, Depends(retrieve_current_company)],
) -> StreamingResponse | None:
    if not retrieved_company.logo:
        return None

    logo = await company_service.retrieve_logo(minio_client=minio_client, object_name=retrieved_company.logo)

    return StreamingResponse(
        content=BytesIO(logo),
    )


@router.post(
    path="/api/v1/me/company/logo",
    status_code=201,
)
async def upload_current_company_logo(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    minio_client: Annotated[Minio, Depends(get_minio_client)],
    retrieved_company: Annotated[Company, Depends(retrieve_current_company)],
    file: Annotated[UploadFile, File()],
) -> None:
    data = await file.read()

    logo = await company_service.upload_logo(
        minio_client=minio_client,
        object_name=retrieved_company.logo or f"{uuid4()}",
        data=BytesIO(data),
        length=len(data),
        content_type=file.content_type,
    )

    await company_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=retrieved_company,
        company=UpdateCompany(logo=logo.object_name),
    )


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
    return await company_service.retrieve_job_by_id(
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
    company_id: int,
    company: UpdateCompany,
) -> Company:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        company_id=company_id,
    )

    if not retrieved_company:
        raise CompanyIdNotFoundException

    return await company_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=retrieved_company,
        company=company,
    )


@router.put(
    path="/api/v1/me/company",
    response_model=UpdatedCompany,
    status_code=200,
)
async def update_current_company(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    company: UpdateCurrentCompany,
) -> Company:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        company_id=retrieved_user.employee.company_id,
    )

    if not retrieved_company:
        raise CompanyIdNotFoundException

    return await company_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=retrieved_company,
        company=company,
    )


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


@router.delete(
    path="/api/v1/me/company",
    response_model=DeletedCurrentCompany,
    status_code=200,
)
async def delete_current_company(
    *,
    retrieved_company: Annotated[Company, Depends(retrieve_current_company)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Company:
    return await company_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_company=retrieved_company,
    )


@router.delete(
    path="/api/v1/me/company/locations/{location_id}",
    response_model=DeletedCurrentCompany,
    status_code=200,
)
async def delete_current_company_location(
    *,
    location_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_company: Annotated[Company, Depends(retrieve_current_company)],
) -> CompanyLocation:
    retrieved_location = await company_service.retrieve_location_by_id(
        sqlmodel_session=sqlmodel_session, company_id=retrieved_company.id, location_id=location_id
    )

    return await company_service.delete_location(
        sqlmodel_session=sqlmodel_session,
        retrieved_location=retrieved_location,
    )


@router.delete(
    path="/api/v1/me/company/links/{link_id}",
    response_model=DeletedCurrentCompany,
    status_code=200,
)
async def delete_current_company_link(
    *,
    link_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_company: Annotated[Company, Depends(retrieve_current_company)],
) -> CompanyLink:
    retrieved_link = await company_service.retrieve_link_by_id(
        sqlmodel_session=sqlmodel_session, company_id=retrieved_company.id, link_id=link_id
    )

    return await company_service.delete_link(
        sqlmodel_session=sqlmodel_session,
        retrieved_link=retrieved_link,
    )


@router.delete(
    path="/api/v1/me/company/employees/{employee_id}",
    response_model=DeletedCurrentCompany,
    status_code=200,
)
async def delete_current_company_employee(
    *,
    employee_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_company: Annotated[Company, Depends(retrieve_current_company)],
) -> Employee:
    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=retrieved_company.id, employee_id=employee_id
    )

    return await employee_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_employee=retrieved_employee,
    )


@router.post(
    path="/api/v1/me/company/employee/invite",
    status_code=200,
)
async def invite_employee(
    *,
    settings: Annotated[Settings, Depends(get_settings)],
    email_client: Annotated[EmailClient, Depends(get_email_client)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    background_tasks: BackgroundTasks,
    employee: EmployeeInvitation,
) -> None:
    token = auth_service.encode_token(
        payload={
            "title": employee.title,
            "email": employee.email,
            "company_id": str(retrieved_user.employee.company_id),
        },
        key=settings.one_time_token_key,
        seconds=settings.one_time_token_expiration,
    )

    context = {
        "company_name": retrieved_user.employee.company.name,
        "link": f"{settings.frontend_base_url}/company/employees/invitation?token={token}",
    }

    await company_service.send_invitation_email(
        email_client=email_client,
        background_tasks=background_tasks,
        context=context,
        from_addr=settings.smtp_email,
        to_addrs=employee.email,
    )


@router.post(
    path="/api/v1/me/company/employee/invitation/accept",
    status_code=200,
)
async def accept_employee_invitation(
    *,
    settings: Annotated[Settings, Depends(get_settings)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    invitation: InvitationAcceptance,
) -> JSONResponse:
    is_verified = auth_service.verify_token(
        token=invitation.token,
        key=settings.one_time_token_key,
    )

    if not is_verified:
        raise InvalidOneTimeTokenException

    _, payload, _ = auth_service.decode_token(token=invitation.token)

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=payload.get("email"),
    )

    if not retrieved_user:
        firstname = "".join(random.choices(string.ascii_letters, k=5)).title()
        lastname = "".join(random.choices(string.ascii_letters, k=5)).title()
        username = f"{firstname}{lastname}{random.randint(1000, 9999)}"
        password = auth_service.encode_password(
            password="".join(
                random.choices(string.ascii_letters + string.digits, k=16),
            ),
        )

        await employee_service.create(
            sqlmodel_session=sqlmodel_session,
            company_id=payload.get("company_id"),
            employee=CreateEmployee(
                title=payload.get("title"),
                company_id=int(payload.get("company_id")),
                user=CreateUser(
                    firstname=firstname,
                    lastname=lastname,
                    username=username,
                    email=payload.get("email"),
                    password=password,
                    verified=True,
                    subscription=CreateSubscription(
                        plan=payload.get("plan"),
                        start_date=datetime.now(UTC).timestamp(),
                        end_date=(datetime.now(UTC) + timedelta(days=15)).timestamp(),
                    ),
                ),
            ),
        )

    retrieved_user = await user_service.retrieve_by_email(sqlmodel_session=sqlmodel_session, email=payload.get("email"))

    retrieved_employee = await employee_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=payload.get("company_id"), employee_id=retrieved_user.employee.id
    )

    if retrieved_employee:
        await employee_service.update(
            sqlmodel_session=sqlmodel_session,
            retrieved_employee=retrieved_employee,
            employee=UpdateEmployee(
                title=payload.get("title"),
                user_id=retrieved_user.employee.id,
                company_id=int(payload.get("company_id")),
            ),
        )

    access_token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    refresh_token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    content = AuthenticationTokens(access_token=access_token, refresh_token=refresh_token)
    response = JSONResponse(content=content.model_dump())

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    return response
