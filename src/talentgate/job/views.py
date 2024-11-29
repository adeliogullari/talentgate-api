from typing import List, Sequence

from sqlmodel import Session
from fastapi import Depends, APIRouter, Query
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.job import service as job_service
from src.talentgate.job.exceptions import IdNotFoundException
from src.talentgate.job.models import (
    Job,
    CreateJob,
    CreatedJob,
    RetrievedJob, JobQueryParameters, UpdatedJob, UpdateJob, DeletedJob,
)

router = APIRouter(tags=["job"])


@router.post(
    path="/api/v1/jobs",
    response_model=CreatedJob,
    status_code=201,
)
async def create_job(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    job: CreateJob,
) -> Job:
    created_job = await job_service.create(
        sqlmodel_session=sqlmodel_session, job=job
    )

    return created_job


@router.get(
    path="/api/v1/jobs/{job_id}",
    response_model=RetrievedJob,
    status_code=200,
)
async def retrieve_job(
    *, job_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise IdNotFoundException

    return retrieved_job


@router.get(
    path="/api/v1/jobs",
    response_model=List[RetrievedJob],
    status_code=200,
)
async def retrieve_jobs(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: JobQueryParameters = Query(),
) -> Sequence[Job]:
    retrieved_job = await job_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_job


@router.put(
    path="/api/v1/jobs/{job_id}",
    response_model=UpdatedJob,
    status_code=200
)
async def update_job(
    *,
    job_id: int,
    job: UpdateJob,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise IdNotFoundException

    updated_job = await job_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_job=retrieved_job, job=job
    )

    return updated_job


@router.delete(
    path="/api/v1/jobs/{job_id}",
    response_model=DeletedJob,
    status_code=200
)
async def delete_job(
    *,
    job_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Job:
    retrieved_job = await job_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, job_id=job_id
    )

    if not retrieved_job:
        raise IdNotFoundException

    deleted_job = await job_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_job=retrieved_job
    )

    return deleted_job
