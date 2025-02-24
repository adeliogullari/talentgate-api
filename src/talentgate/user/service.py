from sqlmodel import select, Session
from typing import Any, Union, Sequence
from pytography import PasswordHashLibrary
from src.talentgate.user.models import (
    UserSubscription,
    User,
    CreateSubscription,
    UpdateSubscription,
    CreateUser,
    UserQueryParameters,
    UpdateUser,
    UpdateCurrentUser,
)
from src.talentgate.auth import service as auth_service
from config import get_settings

settings = get_settings()


async def create_subscription(
    *, sqlmodel_session: Session, subscription: CreateSubscription
) -> UserSubscription:
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


async def upsert_subscription(
    *,
    sqlmodel_session: Session,
    subscription: Union[CreateSubscription, UpdateSubscription],
) -> UserSubscription:
    retrieved_subscription = await retrieve_subscription_by_id(
        sqlmodel_session=sqlmodel_session,
        subscription_id=getattr(subscription, "id", None),
    )
    if retrieved_subscription:
        return await update_subscription(
            sqlmodel_session=sqlmodel_session,
            retrieved_subscription=retrieved_subscription,
            subscription=subscription,
        )
    return await create_subscription(
        sqlmodel_session=sqlmodel_session, subscription=subscription
    )


async def create(*, sqlmodel_session: Session, user: CreateUser) -> User:
    password = auth_service.encode_password(password=user.password)

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


async def retrieve_by_id(*, sqlmodel_session: Session, user_id: int | None) -> User:
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
    *,
    sqlmodel_session: Session,
    retrieved_user: User,
    user: Union[UpdateUser, UpdateCurrentUser],
) -> User:
    if getattr(user, "password", None) is not None:
        retrieved_user.password = auth_service.encode_password(password=user.password)

    if getattr(user, "subscription", None) is not None:
        retrieved_user.subscription = await upsert_subscription(
            sqlmodel_session=sqlmodel_session, subscription=user.subscription
        )

    retrieved_user.sqlmodel_update(
        user.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude={"password", "subscription"},
        )
    )

    sqlmodel_session.add(retrieved_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_user)

    return retrieved_user


async def upsert(
    *,
    sqlmodel_session: Session,
    user: Union[CreateUser, UpdateUser],
) -> User:
    retrieved_user = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=getattr(user, "id", None)
    )

    if retrieved_user:
        return await update(
            sqlmodel_session=sqlmodel_session,
            retrieved_user=retrieved_user,
            user=user,
        )

    return await create(sqlmodel_session=sqlmodel_session, user=user)


async def delete(*, sqlmodel_session: Session, retrieved_user: User) -> User:
    sqlmodel_session.delete(retrieved_user)
    sqlmodel_session.commit()

    return retrieved_user
