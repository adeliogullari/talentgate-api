from sqlmodel import Session
from datetime import datetime, UTC
from src.talentgate.subscription.models import (
    Subscription,
    SubscriptionPlan,
    CreateSubscription,
    SubscriptionQueryParameters,
    UpdateSubscription,
)
from src.talentgate.subscription import service as subscription_service


async def test_create(sqlmodel_session: Session) -> None:
    subscription = CreateSubscription(
        plan=SubscriptionPlan.BASIC,
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC),
    )

    created_subscription = await subscription_service.create(
        sqlmodel_session=sqlmodel_session, subscription=subscription
    )

    assert created_subscription.plan == subscription.plan


async def test_retrieve_by_id(
    sqlmodel_session: Session, subscription: Subscription
) -> None:
    retrieved_subscription = await subscription_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, subscription_id=subscription.id
    )

    assert retrieved_subscription.id == subscription.id


async def test_retrieve_by_query_parameters(
    sqlmodel_session: Session, subscription: Subscription
) -> None:
    query_parameters = SubscriptionQueryParameters(
        offset=0,
        limit=100,
        id=subscription.id,
    )

    retrieved_subscriptions = await subscription_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    assert retrieved_subscriptions[0].id == subscription.id


async def test_update(sqlmodel_session: Session, make_subscription) -> None:
    retrieved_subscription = make_subscription()

    subscription = UpdateSubscription(
        plan=SubscriptionPlan.STANDARD,
        start_date=datetime.now(UTC),
        end_date=datetime.now(UTC),
    )

    updated_subscription = await subscription_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_subscription=retrieved_subscription,
        subscription=subscription,
    )

    assert updated_subscription.id == retrieved_subscription.id
    assert updated_subscription.plan == subscription.plan


async def test_delete(sqlmodel_session, make_subscription) -> None:
    retrieved_subscription = make_subscription()

    deleted_subscription = await subscription_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_subscription=retrieved_subscription
    )

    assert deleted_subscription.id == retrieved_subscription.id
