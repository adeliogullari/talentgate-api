from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any, BinaryIO, Optional, Callable, AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from minio import Minio
from minio.helpers import ObjectWriteResult
from redis import Redis
from redis.typing import KeyT, EncodableT, ExpiryT
from sqlmodel import Session, SQLModel, create_engine
from urllib3 import BaseHTTPResponse, HTTPHeaderDict

from config import Settings, get_settings
from src.talentgate.application.views import router as application_router
from src.talentgate.auth.views import router as auth_router
from src.talentgate.company.views import router as company_router
from src.talentgate.database.service import get_sqlmodel_session, get_redis_client
from src.talentgate.employee.views import router as employee_router
from src.talentgate.job.views import router as job_router
from src.talentgate.storage.service import get_minio_client
from src.talentgate.user.views import router as user_router
from tests.auth.conftest import access_token, headers, refresh_token
from tests.company.conftest import address, company, location, make_company
from tests.employee.conftest import employee, make_employee
from tests.job.conftest import job, make_job
from tests.user.conftest import make_subscription, make_user, subscription, user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


async def start_application() -> FastAPI | None:
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(employee_router)
    app.include_router(auth_router)
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
def redis_client() -> Redis:
    class RedisClient:
        def __init__(self):
            self.store = {}

        async def set(
            self,
            name: KeyT,
            value: EncodableT,
            ex: Optional[ExpiryT] = None,
        ):
            self.store[name] = value
            return True

        async def get(self, name: KeyT):
            return self.store.get(name)

        async def close(self):
            pass

    return RedisClient()


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
            self,
            bucket_name: str,
            object_name: str,
            data: BinaryIO,
            length: int,
        ):
            if bucket_name not in self.buckets:
                self.buckets[bucket_name] = {}
            self.buckets[bucket_name][object_name] = data
            return FileObject(
                bucket_name=bucket_name,
                object_name=object_name,
                data=data,
                length=length,
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
    app: FastAPI,
    sqlmodel_session: Session,
    minio_client: Minio,
) -> AsyncGenerator[TestClient, Any]:
    async def _get_sqlmodel_session() -> AsyncGenerator[Session, Any]:
        yield sqlmodel_session

    async def _get_redis_client() -> AsyncGenerator[Callable[[], Redis], Any]:
        yield redis_client

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
    app.dependency_overrides[get_redis_client] = _get_redis_client
    app.dependency_overrides[get_minio_client] = _get_minio_client
    app.dependency_overrides[get_settings] = _get_settings

    with TestClient(app) as client:
        yield client
