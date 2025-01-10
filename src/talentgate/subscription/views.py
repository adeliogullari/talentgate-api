from sqlmodel import Session
from typing import List, Sequence, Annotated
from fastapi import Depends, APIRouter, Query
from src.talentgate.subscription import service as subscription_service
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.subscription.models import (
    Subscription,
    CreateSubscription,
    CreatedSubscription,
    RetrievedSubscription,
    SubscriptionQueryParameters,
    UpdateSubscription,
    UpdatedSubscription,
    DeletedSubscription,
)

from src.talentgate.subscription.exceptions import (
    IdNotFoundException,
)

router = APIRouter(tags=["subscription"])


@router.post(
    path="/api/v1/subscriptions",
    response_model=CreatedSubscription,
    status_code=201,
)
async def create_subscription(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    subscription: CreateSubscription,
) -> Subscription:
    created_subscription = await subscription_service.create(
        sqlmodel_session=sqlmodel_session, subscription=subscription
    )

    return created_subscription


@router.get(
    path="/api/v1/subscriptions/{subscription_id}",
    response_model=RetrievedSubscription,
    status_code=200,
)
async def retrieve_subscription(
    *, subscription_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Subscription:
    retrieved_subscription = await subscription_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, subscription_id=subscription_id
    )

    if not retrieved_subscription:
        raise IdNotFoundException

    return retrieved_subscription


@router.get(
    path="/api/v1/subscriptions/",
    response_model=List[RetrievedSubscription],
    status_code=200,
)
async def retrieve_subscriptions(
    *,
    query_parameters: Annotated[SubscriptionQueryParameters, Query()],
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Sequence[Subscription]:
    retrieved_subscriptions = await subscription_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_subscriptions


@router.patch(
    path="/api/v1/subscriptions/{subscription_id}",
    response_model=UpdatedSubscription,
    status_code=200,
)
async def update_subscription(
    *,
    subscription_id: int,
    subscription: UpdateSubscription,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Subscription:
    retrieved_subscription = await subscription_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, subscription_id=subscription_id
    )

    if not retrieved_subscription:
        raise IdNotFoundException

    updated_subscription = await subscription_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_subscription=retrieved_subscription,
        subscription=subscription,
    )

    return updated_subscription


@router.delete(
    path="/api/v1/subscriptions/{subscription_id}",
    response_model=DeletedSubscription,
    status_code=200,
)
async def delete_subscription(
    *, subscription_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> Subscription:
    retrieved_subscription = await subscription_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, subscription_id=subscription_id
    )

    if not retrieved_subscription:
        raise IdNotFoundException

    deleted_subscription = await subscription_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_subscription=retrieved_subscription
    )

    return deleted_subscription
