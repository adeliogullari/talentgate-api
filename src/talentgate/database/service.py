from sqlmodel import Session
from sqlmodel import create_engine
from typing import Any, AsyncGenerator
from config import get_settings

settings = get_settings()

schema = settings.postgresql_schema
user = settings.postgresql_user
password = settings.postgresql_password
host = settings.postgresql_host
port = settings.postgresql_port
database = settings.postgresql_database
url = f"{schema}://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(url=url, echo=True)


async def get_sqlmodel_session() -> AsyncGenerator[Session, Any]:
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session
