from typing import Any, Sequence
from sqlmodel import select, Session
from src.talentgate.subscription.models import (
    Subscription,
    CreateSubscription,
    SubscriptionQueryParameters,
    UpdateSubscription,
)
from config import get_settings

settings = get_settings()


async def create(
    *, sqlmodel_session: Session, subscription: CreateSubscription
) -> Subscription:
    created_subscription = Subscription(
        **subscription.model_dump(exclude_unset=True, exclude_none=True),
    )

    sqlmodel_session.add(created_subscription)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_subscription)

    return created_subscription


async def retrieve_by_id(
    *, sqlmodel_session: Session, subscription_id: int
) -> Subscription:
    statement: Any = select(Subscription).where(Subscription.id == subscription_id)

    retrieved_subscription = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_subscription


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: SubscriptionQueryParameters
) -> Sequence[Subscription]:
    offset = query_parameters.offset
    limit = query_parameters.limit
    filters = [
        getattr(Subscription, attr) == value
        for attr, value in query_parameters.model_dump(
            exclude={"offset", "limit"}, exclude_unset=True, exclude_none=True
        ).items()
    ]

    statement: Any = select(Subscription).offset(offset).limit(limit).where(*filters)

    retrieved_subscriptions = sqlmodel_session.exec(statement).all()

    return retrieved_subscriptions


async def update(
    *,
    sqlmodel_session: Session,
    retrieved_subscription: Subscription,
    subscription: UpdateSubscription,
) -> Subscription:
    retrieved_subscription.sqlmodel_update(
        subscription.model_dump(exclude_none=True, exclude_unset=True)
    )

    sqlmodel_session.add(retrieved_subscription)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(retrieved_subscription)

    return retrieved_subscription


async def delete(
    *, sqlmodel_session: Session, retrieved_subscription: Subscription
) -> Subscription:
    sqlmodel_session.delete(retrieved_subscription)
    sqlmodel_session.commit()

    return retrieved_subscription
