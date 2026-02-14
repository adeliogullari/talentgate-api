from collections.abc import Sequence
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, File, Query, UploadFile
from minio import Minio
from sqlmodel import Session

from config import Settings, get_settings
from src.talentgate.application import service as application_service
from src.talentgate.application.exceptions import ApplicationIdNotFoundException, ResumeAlreadyExistsException
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
from src.talentgate.storage.service import get_minio_client
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
    path="/api/v1/jobs/{job_id}/applications/{application_id}/resume",
    status_code=201,
)
async def upload_resume(
    *,
    job_id: int,
    application_id: int,
    file: Annotated[UploadFile, File()],
    settings: Annotated[Settings, Depends(get_settings)],
    minio_client: Annotated[Minio, Depends(get_minio_client)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> None:
    data = await file.read()

    retrieved_application = application_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id, application_id=application_id
    )

    if not retrieved_application:
        raise ApplicationIdNotFoundException

    retrieved_resume = application_service.retrieve_resume(
        minio_client=minio_client,
        bucket_name=settings.minio_default_bucket,
        object_name=f"jobs/{job_id}/applications/{application_id}/resume",
    )

    if retrieved_resume:
        raise ResumeAlreadyExistsException

    await application_service.upload_resume(
        minio_client=minio_client,
        bucket_name=settings.minio_default_bucket,
        object_name=f"jobs/{job_id}/applications/{application_id}/resume",
        data=BytesIO(data),
        length=len(data),
        content_type=file.content_type,
    )


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
