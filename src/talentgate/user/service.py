from collections.abc import Sequence
from io import BytesIO
from typing import Any

from minio import Minio
from minio.helpers import ObjectWriteResult
from sqlmodel import Session, select

from src.talentgate.auth import service as auth_service
from src.talentgate.user.models import (
    CreateUser,
    CreateUserSubscription,
    UpdateCurrentUser,
    UpdateUser,
    UpdateUserSubscription,
    User,
    UserQueryParameters,
    UserSubscription,
)


async def upload_profile(
    *,
    minio_client: Minio,
    bucket_name: str,
    object_name: str,
    data: BytesIO,
    length: int,
    content_type: str,
) -> ObjectWriteResult:
    return minio_client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=data,
        length=length,
        content_type=content_type,
    )


async def retrieve_profile(*, minio_client: Minio, bucket_name: str, object_name: str) -> bytes:
    response = None

    try:
        response = minio_client.get_object(
            bucket_name=bucket_name,
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
    user_id: int,
    subscription: CreateUserSubscription,
) -> UserSubscription:
    created_subscription = UserSubscription(
        **subscription.model_dump(exclude_unset=True, exclude_none=True, exclude={"paddle_subscription_id"}),
        user_id=user_id,
    )

    if "paddle_subscription_id" in subscription.model_fields_set:
        created_subscription.paddle_subscription_id = subscription.paddle_subscription_id

    sqlmodel_session.add(created_subscription)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_subscription)

    return created_subscription


async def retrieve_subscription_by_id(
    *,
    sqlmodel_session: Session,
    user_id: int,
    subscription_id: int,
) -> UserSubscription | None:
    statement: Any = select(UserSubscription).where(
        UserSubscription.user_id == user_id,
        UserSubscription.id == subscription_id,
    )

    return sqlmodel_session.exec(statement).one_or_none()


async def update_subscription(
    *,
    sqlmodel_session: Session,
    retrieved_subscription: UserSubscription,
    subscription: UpdateUserSubscription,
) -> UserSubscription:
    retrieved_subscription.sqlmodel_update(
        subscription.model_dump(exclude_none=True, exclude_unset=True, exclude={"paddle_subscription_id"}),
    )

    if "paddle_subscription_id" in subscription.model_fields_set:
        retrieved_subscription.paddle_subscription_id = subscription.paddle_subscription_id

    sqlmodel_session.add(retrieved_subscription)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_subscription)

    return retrieved_subscription


async def create(*, sqlmodel_session: Session, user: CreateUser) -> User:
    password = auth_service.encode_password(password=user.password)

    created_user = User(
        **user.model_dump(exclude_unset=True, exclude_none=True, exclude={"password", "subscription"}),
        password=password,
    )

    if "subscription" in user.model_fields_set and user.subscription is not None:
        created_user.subscription = await create_subscription(
            sqlmodel_session=sqlmodel_session,
            user_id=created_user.id,
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
        User.__table__.columns[attr] == value
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
    if "password" in user.model_fields_set and user.password is not None:
        retrieved_user.password = auth_service.encode_password(password=user.password)

    if "subscription" in user.model_fields_set and user.subscription is not None:
        retrieved_subscription = await retrieve_subscription_by_id(
            sqlmodel_session=sqlmodel_session, user_id=retrieved_user.id, subscription_id=retrieved_user.subscription.id
        )

        await update_subscription(
            sqlmodel_session=sqlmodel_session,
            retrieved_subscription=retrieved_subscription,
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


async def delete(*, sqlmodel_session: Session, retrieved_user: User) -> User:
    sqlmodel_session.delete(retrieved_user)
    sqlmodel_session.commit()

    return retrieved_user
