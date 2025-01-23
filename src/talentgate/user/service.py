from typing import Any, Sequence
from sqlmodel import select, Session
from pytography import PasswordHashLibrary
from src.talentgate.user.models import (
    UserSubscription,
    User,
    CreateSubscription,
    CreateUser,
    UserQueryParameters,
    UpdateSubscription,
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


async def create_subscription(
    *, sqlmodel_session: Session, subscription: CreateSubscription
):
    created_subscription = UserSubscription(
        **subscription.model_dump(exclude_unset=True, exclude_none=True)
    )

    sqlmodel_session.add(created_subscription)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_subscription)

    return created_subscription


async def retrieve_subscription_by_id(
    *, sqlmodel_session: Session, subscription_id: int
) -> UserSubscription:
    statement: Any = select(UserSubscription).where(
        UserSubscription.id == subscription_id
    )

    retrieved_subscription = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_subscription


async def update_subscription(
    *,
    sqlmodel_session: Session,
    retrieved_subscription: UserSubscription,
    subscription: UpdateSubscription,
) -> UserSubscription:
    retrieved_subscription.sqlmodel_update(
        subscription.model_dump(exclude_none=True, exclude_unset=True)
    )

    sqlmodel_session.add(retrieved_subscription)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_subscription)

    return retrieved_subscription


async def create(*, sqlmodel_session: Session, user: CreateUser) -> User:
    password = encode_password(password=user.password)

    subscription = None
    if getattr(user, "subscription", None) is not None:
        subscription = await create_subscription(
            sqlmodel_session=sqlmodel_session, subscription=user.subscription
        )

    created_user = User(
        **user.model_dump(
            exclude_unset=True, exclude_none=True, exclude={"password", "subscription"}
        ),
        password=password,
        subscription=subscription,
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
    if getattr(user, "subscription", None) is not None:
        retrieved_subscription = await retrieve_subscription_by_id(
            sqlmodel_session=sqlmodel_session,
            subscription_id=retrieved_user.subscription_id,
        )
        await update_subscription(
            sqlmodel_session=sqlmodel_session,
            retrieved_subscription=retrieved_subscription,
            subscription=user.subscription,
        )

    retrieved_user.sqlmodel_update(
        user.model_dump(exclude_none=True, exclude_unset=True, exclude={"subscription"})
    )

    sqlmodel_session.add(retrieved_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_user)

    return retrieved_user


async def delete(*, sqlmodel_session: Session, retrieved_user: User) -> User:
    sqlmodel_session.delete(retrieved_user)
    sqlmodel_session.commit()

    return retrieved_user
