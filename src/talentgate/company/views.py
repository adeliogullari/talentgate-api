from sqlmodel import Session
from typing import List, Sequence, Any
from fastapi import Depends, APIRouter, Query

from src.talentgate.auth.exceptions import InvalidAuthorizationException
from src.talentgate.company.service import add_observer, delete_observer
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.company import service as company_service
from src.talentgate.employee.models import EmployeeTitle
from src.talentgate.job import service as job_service
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
from src.talentgate.company.exceptions import IdNotFoundException
from src.talentgate.job.exceptions import IdNotFoundException as JobIdNotFoundException

from src.talentgate.job.models import (
    RetrievedJob,
    JobQueryParameters,
    Job,
    RetrievedCompanyJob,
    RetrievedCompanyJobs,
)
from src.talentgate.user.models import (
    UserRole,
    User,
    SubscriptionPlan,
    SubscriptionStatus,
)
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["company"])


class CreateCompanyDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        if (user.role == UserRole.ADMIN) or (
            user.subscription.plan == SubscriptionPlan.STANDARD
            and user.subscription.status == SubscriptionStatus.ACTIVE
        ):
            return True
        raise InvalidAuthorizationException


class RetrieveCompanyDependency:
    def __call__(self, company_id: int, user: User = Depends(retrieve_current_user)):
        if (user.role == UserRole.ADMIN) or (
            user.subscription.plan == SubscriptionPlan.STANDARD
            and user.subscription.status == SubscriptionStatus.ACTIVE
            and user.employee.title in [EmployeeTitle.FOUNDER, EmployeeTitle.RECRUITER]
            and user.employee.company_id == company_id
        ):
            return True
        raise InvalidAuthorizationException


class RetrieveCompaniesDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class UpdateCompanyDependency:
    def __call__(self, company_id: int, user: User = Depends(retrieve_current_user)):
        if (user.role == UserRole.ADMIN) or (
            user.subscription.plan == SubscriptionPlan.STANDARD
            and user.subscription.status == SubscriptionStatus.ACTIVE
            and user.employee.title in [EmployeeTitle.FOUNDER, EmployeeTitle.RECRUITER]
            and user.employee.company_id == company_id
        ):
            return True
        raise InvalidAuthorizationException


class DeleteCompanyDependency:
    def __call__(self, company_id: int, user: User = Depends(retrieve_current_user)):
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
    response_model=List[RetrievedCompanyJobs],
    status_code=200,
)
async def retrieved_career_jobs(
    *,
    company_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: JobQueryParameters = Query(),
) -> Sequence[Job]:
    retrieved_jobs = await company_service.retrieve_jobs_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
        company_id=company_id,
    )

    return retrieved_jobs


@router.get(
    path="/api/v1/careers/companies/{company_id}/jobs/{job_id}",
    response_model=RetrievedCompanyJob,
    status_code=200,
)
async def retrieved_careers_job(
    *,
    company_id: int,
    job_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Job:
    retrieved_job = await company_service.retrieve_company_job(
        sqlmodel_session=sqlmodel_session, company_id=company_id, job_id=job_id
    )

    return retrieved_job


@router.get(
    path="/api/v1/companies/{company_id}/jobs",
    response_model=List[RetrievedJob],
    status_code=200,
)
async def retrieved_company_jobs(
    *,
    company_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: JobQueryParameters = Query(),
) -> Sequence[Job]:
    retrieved_jobs = await company_service.retrieve_jobs_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
        company_id=company_id,
    )

    return retrieved_jobs


# COMPANY JOB OBSERVERS Views
@router.put(
    path="/api/v1/companies/{company_id}/jobs/{job_id}/observers",
    response_model=List[Any],
    status_code=200,
)
async def add_company_job_observers(
    *,
    company_id: int,
    job_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    observers: List[int],
) -> Any:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=company_id
    )

    if not retrieved_company:
        raise IdNotFoundException

    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    await add_observer(
        sqlmodel_session=sqlmodel_session,
        retrieved_job=retrieved_job,
        observers=observers,
    )

    return retrieved_job.observers


@router.get(
    path="/api/v1/companies/{company_id}/jobs/{job_id}/observers",
    response_model=List[Any],
    status_code=200,
)
async def get_company_job_observers(
    *,
    company_id: int,
    job_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Any:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=company_id
    )

    if not retrieved_company:
        raise IdNotFoundException

    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    return retrieved_job.observers


@router.delete(
    path="/api/v1/companies/{company_id}/jobs/{job_id}/observers/{employee_id}",
    response_model=List[Any],
    status_code=200,
)
async def delete_company_job_observers(
    *,
    company_id: int,
    job_id: int,
    employee_id: int,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Any:
    retrieved_company = await company_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, company_id=company_id
    )

    if not retrieved_company:
        raise IdNotFoundException

    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    await delete_observer(
        sqlmodel_session=sqlmodel_session,
        retrieved_job=retrieved_job,
        employee_id=employee_id,
    )

    return retrieved_job.observers


@router.post(
    path="/api/v1/companies",
    response_model=CreatedCompany,
    status_code=201,
    dependencies=[Depends(CreateCompanyDependency())],
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
    dependencies=[Depends(RetrieveCompanyDependency())],
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
    dependencies=[Depends(RetrieveCompaniesDependency())],
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
    dependencies=[Depends(UpdateCompanyDependency())],
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
    dependencies=[Depends(DeleteCompanyDependency())],
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
