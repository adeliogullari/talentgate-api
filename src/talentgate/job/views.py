from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.talentgate.auth.exceptions import (
    InvalidAuthorizationException,
)
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.job import service as job_service
from src.talentgate.job.exceptions import IdNotFoundException as JobIdNotFoundException
from src.talentgate.job.models import (
    CreatedJob,
    CreateJob,
    DeletedJob,
    Job,
    JobQueryParameters,
    RetrievedJob,
    UpdatedJob,
    UpdateJob,
)
from src.talentgate.user.models import User, UserRole
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["job"])


class CreateJobDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveJobDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveJobsDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class UpdateJobDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class DeleteJobDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


@router.post(
    path="/api/v1/jobs",
    response_model=CreatedJob,
    status_code=201,
    dependencies=[Depends(CreateJobDependency())],
)
async def create_job(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    job: CreateJob,
) -> Job:
    return await job_service.create(sqlmodel_session=sqlmodel_session, job=job)


@router.get(
    path="/api/v1/jobs/{job_id}",
    response_model=RetrievedJob,
    status_code=200,
    dependencies=[Depends(RetrieveJobDependency())],
)
async def retrieve_job(
    *,
    job_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        job_id=job_id,
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    return retrieved_job


@router.get(
    path="/api/v1/jobs",
    response_model=list[RetrievedJob],
    status_code=200,
    dependencies=[Depends(RetrieveJobsDependency())],
)
async def retrieve_jobs(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    query_parameters: Annotated[JobQueryParameters, Query()],
) -> Sequence[Job]:
    return await job_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
    )


@router.put(
    path="/api/v1/jobs/{job_id}",
    response_model=UpdatedJob,
    status_code=200,
    dependencies=[Depends(UpdateJobDependency())],
)
async def update_job(
    *,
    job_id: int,
    job: UpdateJob,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        job_id=job_id,
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    return await job_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_job=retrieved_job,
        job=job,
    )


@router.delete(
    path="/api/v1/jobs/{job_id}",
    response_model=DeletedJob,
    status_code=200,
    dependencies=[Depends(DeleteJobDependency())],
)
async def delete_job(
    *,
    job_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        job_id=job_id,
    )

    if not retrieved_job:
        raise JobIdNotFoundException

    return await job_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_job=retrieved_job,
    )
