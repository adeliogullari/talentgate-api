from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import Engine
from sqlmodel import Session, create_engine
from redis import Redis
from config import get_settings

settings = get_settings()


def get_postgres_connection_string(
    schema: str, user: str, password: str, host: str, port: str, database: str
) -> str:
    return f"{schema}://{user}:{password}@{host}:{port}/{database}"


def get_sqlmodel_engine() -> Engine:
    url = get_postgres_connection_string(
        schema=settings.postgres_schema,
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
        port=settings.postgres_port,
        database=settings.postgres_db,
    )
    return create_engine(url=url, echo=True)


async def get_sqlmodel_session() -> AsyncGenerator[Session, Any]:
    engine = get_sqlmodel_engine()
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session


async def get_redis_client() -> AsyncGenerator[Redis, Any]:
    yield Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        username=settings.redis_username,
        password=settings.redis_password,
        decode_responses=True,
    )
