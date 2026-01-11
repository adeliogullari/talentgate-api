from datetime import UTC, datetime, timedelta
from io import BytesIO
from uuid import uuid4

import pytest
from minio import Minio
from sqlmodel import Session

from src.talentgate.user import service as user_service
from src.talentgate.user.models import (
    CreateUserSubscription,
    CreateUser,
    UserSubscription,
    UserSubscriptionPlan,
    UserSubscriptionStatus,
    UpdateUserSubscription,
    UpdateUser,
    User,
    UserQueryParameters,
    UserRole,
)


async def test_upload_profile(minio_client: Minio):
    object_name = "users/1/profile"
    data = BytesIO(b"data")

    await user_service.upload_profile(
        minio_client=minio_client,
        bucket_name="talentgate",
        object_name=object_name,
        data=data,
        length=4,
        content_type="file",
    )

    data = minio_client.get_object(bucket_name="talentgate", object_name=object_name)

    assert data == data


async def test_retrieve_profile(minio_client: Minio):
    object_name = "users/1/profile"
    data = b"data"

    minio_client.put_object(
        bucket_name="talentgate",
        object_name=object_name,
        data=BytesIO(data),
        length=4,
        content_type="file",
    )

    retrieved_profile = await user_service.retrieve_profile(
        minio_client=minio_client, bucket_name="talentgate", object_name=object_name
    )

    assert retrieved_profile == data


async def test_create_subscription(sqlmodel_session: Session, user: User) -> None:
    subscription = CreateUserSubscription(
        paddle_subscription_id=str(uuid4()),
        plan=UserSubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    created_subscription = await user_service.create_subscription(
        sqlmodel_session=sqlmodel_session,
        user_id=user.id,
        subscription=subscription,
    )

    assert created_subscription.plan == subscription.plan


async def test_retrieve_subscription_by_id(
    sqlmodel_session: Session,
    user_subscription: UserSubscription,
) -> None:
    retrieved_subscription = await user_service.retrieve_subscription_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=user_subscription.user_id,
        subscription_id=user_subscription.id,
    )

    assert retrieved_subscription.id == user_subscription.id


@pytest.mark.parametrize(
    "user_subscription",
    [
        {
            "start_date": (datetime.now(UTC) - timedelta(days=2)).timestamp(),
            "end_date": (datetime.now(UTC) + timedelta(days=1)).timestamp(),
        },
    ],
    indirect=True,
)
async def test_retrieve_subscription_with_active_status(
    sqlmodel_session: Session,
    user_subscription: UserSubscription,
) -> None:
    retrieved_subscription = await user_service.retrieve_subscription_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=user_subscription.user_id,
        subscription_id=user_subscription.id,
    )

    assert retrieved_subscription.id == user_subscription.id
    assert retrieved_subscription.status == UserSubscriptionStatus.ACTIVE


@pytest.mark.parametrize(
    "user_subscription",
    [
        {
            "start_date": (datetime.now(UTC) - timedelta(days=2)).timestamp(),
            "end_date": (datetime.now(UTC) - timedelta(days=1)).timestamp(),
        },
    ],
    indirect=True,
)
async def test_retrieve_subscription_with_expired_status(
    sqlmodel_session: Session,
    user_subscription: UserSubscription,
) -> None:
    retrieved_subscription = await user_service.retrieve_subscription_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=user_subscription.user_id,
        subscription_id=user_subscription.id,
    )

    assert retrieved_subscription.id == user_subscription.id
    assert retrieved_subscription.status == UserSubscriptionStatus.EXPIRED


async def test_update_subscription(
    sqlmodel_session: Session,
    make_user_subscription,
) -> None:
    retrieved_subscription = make_user_subscription()

    subscription = UpdateUserSubscription(
        paddle_subscription_id=str(uuid4()),
        plan=UserSubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    updated_subscription = await user_service.update_subscription(
        sqlmodel_session=sqlmodel_session,
        retrieved_subscription=retrieved_subscription,
        subscription=subscription,
    )

    assert updated_subscription.id == retrieved_subscription.id
    assert updated_subscription.plan == subscription.plan


async def test_create(sqlmodel_session: Session) -> None:
    subscription = CreateUserSubscription(
        plan=UserSubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    user = CreateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ADMIN,
        subscription=subscription,
    )

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session,
        user=user,
    )

    assert created_user.email == user.email
    assert created_user.subscription.plan == subscription.plan


async def test_retrieve_by_id(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=user.id,
    )

    assert retrieved_user.id == user.id


async def test_retrieve_by_username(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session,
        username=user.username,
    )

    assert retrieved_user.username == user.username


async def test_retrieve_by_email(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=user.email,
    )

    assert retrieved_user.email == user.email


async def test_retrieve_by_query_parameters(
    sqlmodel_session: Session,
    user: User,
) -> None:
    query_parameters = UserQueryParameters(
        offset=0,
        limit=100,
        id=user.id,
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        verified=user.verified,
        role=user.role,
    )

    retrieved_users = await user_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
    )

    assert retrieved_users[0].id == user.id


async def test_update(sqlmodel_session: Session, make_user) -> None:
    retrieved_user = make_user()

    subscription = UpdateUserSubscription(
        paddle_subscription_id=str(uuid4()),
        plan=UserSubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    user = UpdateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ADMIN,
        subscription=subscription,
    )

    updated_user = await user_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
        user=user,
    )

    assert updated_user.id == retrieved_user.id
    assert updated_user.email == user.email
    assert updated_user.subscription.plan == subscription.plan


async def test_delete(sqlmodel_session, make_user) -> None:
    retrieved_user = make_user()

    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
    )

    assert deleted_user.id == retrieved_user.id
