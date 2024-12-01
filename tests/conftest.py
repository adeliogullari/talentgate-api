import pytest
from typing import Any, AsyncGenerator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from config import Settings, get_settings


from src.talentgate.user.views import router as user_router
from src.talentgate.employee.views import router as employee_router
from src.talentgate.auth.views import router as auth_router
from src.talentgate.location.views import router as location_router
from src.talentgate.applicant.views import router as applicant_router
from src.talentgate.application.views import router as application_router
from src.talentgate.job.views import router as job_router
from src.talentgate.observer.views import router as observer_router
from src.talentgate.database.service import get_sqlmodel_session
from tests.employee.conftest import employee, make_employee
from tests.job.conftest import job, make_job

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
    app.include_router(observer_router)
    return app


@pytest.fixture
async def app() -> AsyncGenerator[FastAPI, Any] | None:
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
async def client(
    app: FastAPI, sqlmodel_session: Session
) -> AsyncGenerator[TestClient, Any]:
    async def _get_sqlmodel_session() -> AsyncGenerator[Session, Any]:
        yield sqlmodel_session

    async def _get_settings() -> AsyncGenerator[Settings, Any]:
        yield Settings(
            password_hash_algorithm="scrypt",
            message_digest_algorithm="blake2b",
            access_token_expiration_minutes=60,
            access_token_key="SJ6nWJtM737AZWevVdDEr4Fh0GmoyR8k",
            refresh_token_expiration_days=90,
            refresh_token_key="SJ6nWJtM737AZWevVdDEr4Fh0GmoyR8k",
        )

    app.dependency_overrides[get_sqlmodel_session] = _get_sqlmodel_session
    app.dependency_overrides[get_settings] = _get_settings

    with TestClient(app) as client:
        yield client
