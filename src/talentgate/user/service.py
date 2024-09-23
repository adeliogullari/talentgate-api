from typing import Any, Sequence
from sqlmodel import select, Session
from src.talentgate.auth.crypto.password.library import PasswordHashLibrary
from src.talentgate.user.models import (
    User,
    CreateUserRequest,
    UserQueryParameters,
    UpdateUserRequest,
)
from config import get_settings

settings = get_settings()
password_hash_library = PasswordHashLibrary(settings.password_hash_algorithm)


async def create(*, sqlmodel_session: Session, user: CreateUserRequest) -> User:
    password = password_hash_library.encode(password=user.password)

    created_user = User(**user.model_dump(exclude_unset=True, exclude={'password'}), password=password)

    sqlmodel_session.add(created_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_user)

    return created_user


async def retrieve_by_id(*, sqlmodel_session: Session, user_id: int) -> User:
    statement: Any = select(User).where(User.id == user_id)

    retrieved_user = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_user


async def retrieve_by_username(*, sqlmodel_session: Session, username: str) -> User:
    statement: Any = select(User).where(User.username == username)

    retrieved_user = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_user


async def retrieve_by_email(*, sqlmodel_session: Session, email: str) -> User:
    statement: Any = select(User).where(User.email == email)

    retrieved_user = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_user


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: UserQueryParameters
) -> Sequence[User]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    print('zekeriya')
    print(query_parameters)
    filters = {
        getattr(User, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        )
    }

    statement: Any = select(User).offset(offset).limit(limit).where(*filters)

    retrieved_user = sqlmodel_session.exec(statement).all()

    return retrieved_user


async def update(
    *, sqlmodel_session: Session, retrieved_user: User, user: UpdateUserRequest
) -> User:
    user.password = password_hash_library.encode(password=user.password)
    retrieved_user.sqlmodel_update(user)

    sqlmodel_session.add(retrieved_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_user)

    return retrieved_user


async def delete(*, sqlmodel_session: Session, retrieved_user: User) -> User:
    sqlmodel_session.delete(retrieved_user)
    sqlmodel_session.commit()

    return retrieved_user
