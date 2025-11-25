from collections.abc import Sequence
from io import BytesIO
from typing import Any

from minio import Minio
from minio.helpers import ObjectWriteResult
from sqlmodel import Session, select

from config import get_settings
from src.talentgate.auth import service as auth_service
from src.talentgate.user.models import (
    CreateSubscription,
    CreateUser,
    UpdateCurrentUser,
    UpdateSubscription,
    UpdateUser,
    UpsertSubscription,
    UpsertUser,
    User,
    UserQueryParameters,
    UserSubscription,
)

settings = get_settings()


async def upload_profile(
    *,
    minio_client: Minio,
    object_name: str,
    data: BytesIO,
    length: int,
    content_type: str,
) -> ObjectWriteResult:
    return minio_client.put_object(
        bucket_name="profile",
        object_name=object_name,
        data=data,
        length=length,
        content_type=content_type,
    )


async def retrieve_profile(*, minio_client: Minio, object_name: str) -> bytes:
    response = None

    try:
        response = minio_client.get_object(
            bucket_name="profile",
            object_name=object_name,
        )
        data = response.data
    finally:
        if response:
            response.close()
            response.release_conn()

    return data


async def create_subscription(
    *,
    sqlmodel_session: Session,
    subscription: CreateSubscription,
) -> UserSubscription:
    created_subscription = UserSubscription(
        **subscription.model_dump(
            exclude_unset=True, exclude_none=True, exclude={"paddle_subscription_id"}
        ),
    )

    if hasattr(subscription, "paddle_subscription_id"):
        created_subscription.paddle_subscription_id = (
            subscription.paddle_subscription_id
        )

    sqlmodel_session.add(created_subscription)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_subscription)

    return created_subscription


async def retrieve_subscription_by_id(
    *,
    sqlmodel_session: Session,
    subscription_id: int,
) -> UserSubscription:
    statement: Any = select(UserSubscription).where(
        UserSubscription.id == subscription_id,
    )

    return sqlmodel_session.exec(statement).one_or_none()


async def update_subscription(
    *,
    sqlmodel_session: Session,
    retrieved_subscription: UserSubscription,
    subscription: UpdateSubscription,
) -> UserSubscription:
    if hasattr(subscription, "paddle_subscription_id"):
        retrieved_subscription.paddle_subscription_id = (
            subscription.paddle_subscription_id
        )

    retrieved_subscription.sqlmodel_update(
        subscription.model_dump(
            exclude_none=True, exclude_unset=True, exclude={"paddle_subscription_id"}
        ),
    )

    sqlmodel_session.add(retrieved_subscription)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_subscription)

    return retrieved_subscription


async def upsert_subscription(
    *,
    sqlmodel_session: Session,
    subscription: UpsertSubscription,
) -> UserSubscription:
    subscription_id = getattr(subscription, "id", None)

    retrieved_subscription = await retrieve_subscription_by_id(
        sqlmodel_session=sqlmodel_session,
        subscription_id=subscription_id,
    )

    if retrieved_subscription:
        return await update_subscription(
            sqlmodel_session=sqlmodel_session,
            retrieved_subscription=retrieved_subscription,
            subscription=UpdateSubscription(
                **subscription.model_dump(
                    exclude_none=True, exclude_unset=True, exclude={"id"}
                )
            ),
        )

    return await create_subscription(
        sqlmodel_session=sqlmodel_session,
        subscription=CreateSubscription(
            **subscription.model_dump(
                exclude_none=True, exclude_unset=True, exclude={"id"}
            )
        ),
    )


async def create(*, sqlmodel_session: Session, user: CreateUser) -> User:
    password = auth_service.encode_password(password=user.password)

    created_user = User(
        **user.model_dump(
            exclude_unset=True, exclude_none=True, exclude={"password", "subscription"}
        ),
        password=password,
    )

    if getattr(user, "subscription", None):
        created_user.subscription = await upsert_subscription(
            sqlmodel_session=sqlmodel_session,
            subscription=user.subscription,
        )

    sqlmodel_session.add(created_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_user)

    return created_user


async def retrieve_by_id(*, sqlmodel_session: Session, user_id: int | None) -> User:
    statement: Any = select(User).where(User.id == user_id)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_username(*, sqlmodel_session: Session, username: str) -> User:
    statement: Any = select(User).where(User.username == username)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_email(*, sqlmodel_session: Session, email: str) -> User:
    statement: Any = select(User).where(User.email == email)

    return sqlmodel_session.exec(statement).one_or_none()


async def retrieve_by_query_parameters(
    *,
    sqlmodel_session: Session,
    query_parameters: UserQueryParameters,
) -> Sequence[User]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = [
        getattr(User, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"},
            exclude_unset=True,
            exclude_none=True,
        ).items()
    ]

    statement: Any = select(User).offset(offset).limit(limit).where(*filters)

    return sqlmodel_session.exec(statement).all()


async def update(
    *,
    sqlmodel_session: Session,
    retrieved_user: User,
    user: UpdateUser | UpdateCurrentUser,
) -> User:
    if getattr(user, "password", None):
        retrieved_user.password = auth_service.encode_password(password=user.password)

    if getattr(user, "subscription", None):
        retrieved_user.subscription = await upsert_subscription(
            sqlmodel_session=sqlmodel_session,
            subscription=user.subscription,
        )

    retrieved_user.sqlmodel_update(
        user.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude={"password", "subscription"},
        ),
    )

    sqlmodel_session.add(retrieved_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_user)

    return retrieved_user


async def upsert(
    *,
    sqlmodel_session: Session,
    user: UpsertUser,
) -> User:
    user_id = getattr(user, "id", None)

    retrieved_user = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=user_id,
    )

    if retrieved_user:
        return await update(
            sqlmodel_session=sqlmodel_session,
            retrieved_user=retrieved_user,
            user=UpdateUser(
                **user.model_dump(
                    exclude_none=True,
                    exclude_unset=True,
                    exclude={"id"},
                ),
            ),
        )

    return await create(
        sqlmodel_session=sqlmodel_session,
        user=CreateUser(
            **user.model_dump(
                exclude_none=True,
                exclude_unset=True,
                exclude={"id"},
            ),
        ),
    )


async def delete(*, sqlmodel_session: Session, retrieved_user: User) -> User:
    sqlmodel_session.delete(retrieved_user)
    sqlmodel_session.commit()

    return retrieved_user
