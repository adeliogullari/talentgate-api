from typing import Any, Sequence
from sqlmodel import select, Session
from pytography import PasswordHashLibrary
from src.talentgate.user.models import (
    User,
    CreateUser,
    UserQueryParameters,
    UpdateUser,
)
from config import get_settings

settings = get_settings()


def encode_password(password: str):
    return PasswordHashLibrary.encode(password=password)


def verify_password(password: str, encoded_password: str):
    return PasswordHashLibrary.verify(
        password=password, encoded_password=encoded_password
    )


async def create(*, sqlmodel_session: Session, user: CreateUser) -> User:
    password = encode_password(password=user.password)

    created_user = User(
        **user.model_dump(
            exclude_unset=True, exclude_none=True, exclude={"password", "subscription"}
        ),
        password=password,
    )

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
    filters = [
        getattr(User, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        ).items()
    ]

    statement: Any = select(User).offset(offset).limit(limit).where(*filters)

    retrieved_users = sqlmodel_session.exec(statement).all()

    return retrieved_users


async def update(
    *, sqlmodel_session: Session, retrieved_user: User, user: UpdateUser
) -> User:
    retrieved_user.sqlmodel_update(
        user.model_dump(exclude_none=True, exclude_unset=True)
    )

    sqlmodel_session.add(retrieved_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_user)

    return retrieved_user


async def delete(*, sqlmodel_session: Session, retrieved_user: User) -> User:
    sqlmodel_session.delete(retrieved_user)
    sqlmodel_session.commit()

    return retrieved_user
