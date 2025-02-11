import pytest
from sqlmodel import Session
from datetime import datetime, timedelta, UTC
from src.talentgate.user.models import (
    SubscriptionPlan,
    SubscriptionStatus,
    UserSubscription,
    CreateSubscription,
    UpdateSubscription,
    UserRole,
    User,
    CreateUser,
    UserQueryParameters,
    UpdateUser,
)
from src.talentgate.user import service as user_service


async def test_create_subscription(sqlmodel_session: Session) -> None:
    subscription = CreateSubscription(
        plan=SubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    created_subscription = await user_service.create_subscription(
        sqlmodel_session=sqlmodel_session, subscription=subscription
    )

    assert created_subscription.plan == subscription.plan


async def test_retrieve_subscription_by_id(
    sqlmodel_session: Session, subscription: UserSubscription
) -> None:
    retrieved_subscription = await user_service.retrieve_subscription_by_id(
        sqlmodel_session=sqlmodel_session, subscription_id=subscription.id
    )

    assert retrieved_subscription.id == subscription.id


@pytest.mark.parametrize(
    "subscription",
    [
        {
            "start_date": (datetime.now(UTC) - timedelta(days=2)).timestamp(),
            "end_date": (datetime.now(UTC) + timedelta(days=1)).timestamp(),
        }
    ],
    indirect=True,
)
async def test_retrieve_subscription_with_active_status(
    sqlmodel_session: Session, subscription: UserSubscription
) -> None:
    retrieved_subscription = await user_service.retrieve_subscription_by_id(
        sqlmodel_session=sqlmodel_session, subscription_id=subscription.id
    )

    assert retrieved_subscription.id == subscription.id
    assert retrieved_subscription.status == SubscriptionStatus.ACTIVE


@pytest.mark.parametrize(
    "subscription",
    [
        {
            "start_date": (datetime.now(UTC) - timedelta(days=2)).timestamp(),
            "end_date": (datetime.now(UTC) - timedelta(days=1)).timestamp(),
        }
    ],
    indirect=True,
)
async def test_retrieve_subscription_with_expired_status(
    sqlmodel_session: Session, subscription: UserSubscription
) -> None:
    retrieved_subscription = await user_service.retrieve_subscription_by_id(
        sqlmodel_session=sqlmodel_session, subscription_id=subscription.id
    )

    assert retrieved_subscription.id == subscription.id
    assert retrieved_subscription.status == SubscriptionStatus.EXPIRED


async def test_update_subscription(
    sqlmodel_session: Session, make_subscription
) -> None:
    retrieved_subscription = make_subscription()

    subscription = UpdateSubscription(
        plan=SubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    updated_subscription = await user_service.update_subscription(
        sqlmodel_session=sqlmodel_session,
        retrieved_subscription=retrieved_subscription,
        subscription=subscription,
    )

    assert updated_subscription.plan == subscription.plan


async def test_upsert_create_subscription(sqlmodel_session: Session) -> None:
    subscription = CreateSubscription(
        plan=SubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    created_subscription = await user_service.upsert_subscription(
        sqlmodel_session=sqlmodel_session, subscription=subscription
    )

    assert created_subscription.plan == subscription.plan


async def test_upsert_update_subscription(
    sqlmodel_session: Session, make_subscription
) -> None:
    retrieved_subscription = make_subscription()

    subscription = UpdateSubscription(
        id=retrieved_subscription.id,
        plan=SubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    updated_subscription = await user_service.upsert_subscription(
        sqlmodel_session=sqlmodel_session,
        subscription=subscription,
    )

    assert updated_subscription.id == subscription.id
    assert updated_subscription.plan == subscription.plan


async def test_create(sqlmodel_session: Session) -> None:
    subscription = CreateSubscription(
        plan=SubscriptionPlan.STANDARD,
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
        sqlmodel_session=sqlmodel_session, user=user
    )

    assert created_user.email == user.email
    assert created_user.subscription.plan == subscription.plan


async def test_retrieve_by_id(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user.id
    )

    assert retrieved_user.id == user.id


async def test_retrieve_by_username(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session, username=user.username
    )

    assert retrieved_user.username == user.username


async def test_retrieve_by_email(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=user.email
    )

    assert retrieved_user.email == user.email


async def test_retrieve_by_query_parameters(
    sqlmodel_session: Session, user: User
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
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    assert retrieved_users[0].id == user.id


async def test_upsert_create(sqlmodel_session: Session) -> None:
    subscription = CreateSubscription(
        plan=SubscriptionPlan.STANDARD,
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

    created_user = await user_service.upsert(
        sqlmodel_session=sqlmodel_session, user=user
    )

    assert created_user.email == user.email
    assert created_user.subscription.plan == subscription.plan


async def test_update(sqlmodel_session: Session, make_user, subscription) -> None:
    retrieved_user = make_user()

    subscription = UpdateSubscription(
        id=retrieved_user.subscription_id,
        plan=SubscriptionPlan.STANDARD,
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
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    assert updated_user.subscription_id == subscription.id
    assert updated_user.subscription.plan == subscription.plan


async def test_upsert_update(sqlmodel_session: Session, make_user) -> None:
    retrieved_user = make_user()

    subscription = UpdateSubscription(
        id=retrieved_user.subscription_id,
        plan=SubscriptionPlan.STANDARD,
        start_date=(datetime.now(UTC) - timedelta(days=2)).timestamp(),
        end_date=(datetime.now(UTC) + timedelta(days=1)).timestamp(),
    )

    user = UpdateUser(
        id=retrieved_user.id,
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        role=UserRole.ADMIN,
        subscription=subscription,
    )

    updated_user = await user_service.upsert(
        sqlmodel_session=sqlmodel_session, user=user
    )

    assert updated_user.id == user.id
    assert updated_user.subscription.id == subscription.id


async def test_delete(sqlmodel_session, make_user) -> None:
    retrieved_user = make_user()

    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    assert deleted_user.id == retrieved_user.id
