import pytest
from typing import Any, AsyncGenerator, BinaryIO
from fastapi import FastAPI
from fastapi.testclient import TestClient
from minio import Minio
from minio.helpers import ObjectWriteResult
from sqlmodel import Session, SQLModel, create_engine
from urllib3 import BaseHTTPResponse, HTTPHeaderDict
from dataclasses import dataclass

from config import Settings, get_settings

from tests.auth.conftest import headers, access_token, refresh_token
from tests.user.conftest import make_subscription, subscription, make_user, user
from tests.employee.conftest import make_employee, employee
from tests.job.conftest import make_job, job
from tests.company.conftest import make_company, company, location, address

from src.talentgate.user.views import router as user_router
from src.talentgate.employee.views import router as employee_router
from src.talentgate.auth.views import router as auth_router
from src.talentgate.location.views import router as location_router
from src.talentgate.applicant.views import router as applicant_router
from src.talentgate.application.views import router as application_router
from src.talentgate.job.views import router as job_router
from src.talentgate.company.views import router as company_router
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.storage.service import get_minio_client

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


async def start_application() -> FastAPI | None:
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(employee_router)
    app.include_router(auth_router)
    app.include_router(location_router)
    app.include_router(applicant_router)
    app.include_router(application_router)
    app.include_router(job_router)
    app.include_router(company_router)
    return app


@pytest.fixture
async def app() -> AsyncGenerator[FastAPI | None, Any]:
    SQLModel.metadata.create_all(bind=engine)
    _app = await start_application()
    yield _app
    SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture
async def sqlmodel_session(app: FastAPI) -> AsyncGenerator[Session, Any]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    SQLModel.metadata.create_all(engine)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def minio_client() -> Minio:
    @dataclass
    class FileObject:
        bucket_name: str
        object_name: str
        data: BinaryIO
        length: int

    class FileWriteResult:
        def __init__(
            self,
            bucket_name: str,
            object_name: str,
        ):
            self._data = None

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, value):
            self._data = value

        def close(self):
            return None

        def release_conn(self):
            return None

    class MinioClient:
        def __init__(self):
            self.buckets = {}

        def put_object(
            self, bucket_name: str, object_name: str, data: BinaryIO, length: int
        ):
            if bucket_name not in self.buckets:
                self.buckets[bucket_name] = {}
            self.buckets[bucket_name][object_name] = data
            return FileObject(
                **{
                    "bucket_name": bucket_name,
                    "object_name": object_name,
                    "data": data,
                    "length": length,
                }
            )

        def get_object(self, bucket_name: str, object_name: str):
            result = FileWriteResult(bucket_name=bucket_name, object_name=object_name)
            result.data = self.buckets[bucket_name][object_name]
            return result

        def upload_file(self, bucket_name: str, file_name: str, data: bytes) -> None:
            if bucket_name not in self.buckets:
                self.buckets[bucket_name] = {}
            self.buckets[bucket_name][file_name] = data

        def list_files(self, bucket_name: str):
            return list(self.buckets.get(bucket_name, {}).keys())

        def download_file(self, bucket_name: str, file_name: str) -> bytes:
            return self.buckets.get(bucket_name, {}).get(file_name, b"")

    return MinioClient()


@pytest.fixture
async def client(
    app: FastAPI, sqlmodel_session: Session, minio_client: Minio
) -> AsyncGenerator[TestClient, Any]:
    async def _get_sqlmodel_session() -> AsyncGenerator[Session, Any]:
        yield sqlmodel_session

    async def _get_minio_client() -> AsyncGenerator[Minio, Any]:
        yield minio_client

    async def _get_settings() -> AsyncGenerator[Settings, Any]:
        yield Settings(
            password_hash_algorithm="scrypt",
            message_digest_algorithm="blake2b",
            access_token_expiration=7200,
            access_token_key="SJ6nWJtM737AZWevVdDEr4Fh0GmoyR8k",
            refresh_token_expiration=86400,
            refresh_token_key="SJ6nWJtM737AZWevVdDEr4Fh0GmoyR8k",
        )

    app.dependency_overrides[get_sqlmodel_session] = _get_sqlmodel_session
    app.dependency_overrides[get_minio_client] = _get_minio_client
    app.dependency_overrides[get_settings] = _get_settings

    with TestClient(app) as client:
        yield client
