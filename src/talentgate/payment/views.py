from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, APIRouter
from paddle_billing import Client
from paddle_billing.Entities.Shared import TransactionStatus
from paddle_billing.Entities.Subscriptions import SubscriptionStatus
from paddle_billing.Notifications.Entities.Shared import PaymentAttemptStatus
from pydantic import BaseModel
from sqlmodel import Session

from config import Settings, get_settings
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.payment.exceptions import (
    InactiveSubscriptionException,
    IncompleteTransactionException,
    InvalidProductIdException,
    UnauthorizedPaymentException,
)
from src.talentgate.payment.service import get_paddle_client
from src.talentgate.user import service as user_service
from src.talentgate.user.enums import SubscriptionPlan
from src.talentgate.user.models import UpdateSubscription, User
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["payment"])


class PaymentCheckout(BaseModel):
    transaction_id: str | None = None


@router.post("/payment/checkout")
async def payment_checkout(
    *,
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    checkout: PaymentCheckout,
) -> dict[str, str | None]:
    transaction = paddle_client.transactions.get(transaction_id=checkout.transaction_id)
    subscription = paddle_client.subscriptions.get(
        subscription_id=transaction.subscription_id
    )

    if not transaction.status == TransactionStatus.Completed:
        raise IncompleteTransactionException

    if not (
        transaction.payments
        and transaction.payments[0].status == PaymentAttemptStatus.Authorized
    ):
        raise UnauthorizedPaymentException

    if not subscription.status == SubscriptionStatus.Active:
        raise InactiveSubscriptionException

    start_date = (
        datetime.strptime(
            subscription["billing_cycle"]["start_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        .replace(tzinfo=UTC)
        .timestamp()
    )
    end_date = (
        datetime.strptime(
            subscription["billing_cycle"]["end_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        .replace(tzinfo=UTC)
        .timestamp()
    )

    product_subscription = {
        settings.paddle_standard_product_id: SubscriptionPlan.STANDARD.value
    }

    if not (
        transaction.items and transaction.items[0].product.id in product_subscription
    ):
        raise InvalidProductIdException

    plan = product_subscription.get(transaction.items[0].product.id)

    await user_service.update_subscription(
        sqlmodel_session=sqlmodel_session,
        retrieved_subscription=retrieved_user.subscription,
        subscription=UpdateSubscription(
            plan=plan, start_date=start_date, end_date=end_date
        ),
    )

    return {
        "transaction_id": checkout.transaction_id,
        "subscription_id": checkout.subscription_id,
        "plan": plan,
        "start_date": start_date,
        "end_date": end_date,
    }
