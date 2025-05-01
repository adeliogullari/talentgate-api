from collections.abc import AsyncGenerator
from typing import Any

from sqlmodel import Session, create_engine

from config import get_settings

settings = get_settings()

schema = settings.postgres_schema
user = settings.postgres_user
password = settings.postgres_password
host = settings.postgres_host
port = settings.postgres_port
database = settings.postgres_db
url = f"{schema}://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(url=url, echo=True)


async def get_sqlmodel_session() -> AsyncGenerator[Session, Any]:
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session
