import asyncio
from datetime import UTC

from paddle_billing import Client, Environment, Options
from paddle_billing.Entities.Shared import PaymentAttemptStatus, TransactionStatus
from paddle_billing.Entities.Subscription import Subscription
from paddle_billing.Entities.Subscriptions import (
    SubscriptionItemStatus,
    SubscriptionStatus,
)
from paddle_billing.Entities.Transaction import Transaction
from sqlmodel import Session

from config import get_settings
from src.talentgate.user import service as user_service
from src.talentgate.user.enums import SubscriptionPlan
from src.talentgate.user.models import UpdateSubscription, User

settings = get_settings()

product_subscription = {
    settings.paddle_standard_product_id: SubscriptionPlan.STANDARD.value
}


def get_paddle_client() -> Client:
    return Client(
        api_key=settings.paddle_api_secret_key,
        options=Options(Environment.SANDBOX),
    )


async def verify_transaction(transaction: Transaction | None) -> bool:
    payment = transaction.payments[0] if transaction.payments else None

    return (
        transaction
        and transaction.status == TransactionStatus.Completed
        and payment
        and payment.status == PaymentAttemptStatus.Captured
    )


async def verify_subscription(subscription: Subscription | None) -> bool:
    item = subscription.items[0] if subscription.items else None

    return (
        subscription
        and subscription.status == SubscriptionStatus.Active
        and item
        and item.status == SubscriptionItemStatus.Active
    )


async def update_subscription(
    sqlmodel_session: Session,
    subscription: Subscription,
    retrieved_user: User,
) -> None:
    start_date = subscription.current_billing_period.starts_at.replace(
        tzinfo=UTC
    ).timestamp()
    end_date = subscription.current_billing_period.ends_at.replace(
        tzinfo=UTC
    ).timestamp()

    plan = product_subscription.get(subscription.items[0].product.id)

    await user_service.update_subscription(
        sqlmodel_session=sqlmodel_session,
        retrieved_subscription=retrieved_user.subscription,
        subscription=UpdateSubscription(
            plan=plan, start_date=start_date, end_date=end_date
        ),
    )


async def verify_payment(
    paddle_client: Client,
    sqlmodel_session: Session,
    retrieved_user: User,
    transaction_id: str,
    attempt: int = 0,
    retry: int = 5,
    interval: float = 10,
) -> bool:
    await asyncio.sleep(interval)

    transaction = paddle_client.transactions.get(transaction_id=transaction_id)
    subscription = paddle_client.subscriptions.get(
        subscription_id=transaction.subscription_id
    )

    is_transaction_verified = verify_transaction(transaction=transaction)
    is_subscription_verified = verify_subscription(subscription=subscription)

    is_payment_verified = is_transaction_verified and is_subscription_verified

    if is_payment_verified:
        await update_subscription(
            sqlmodel_session=sqlmodel_session,
            subscription=subscription,
            retrieved_user=retrieved_user,
        )
        return True

    if attempt >= retry:
        return False

    attempt += 1

    return await verify_payment(
        paddle_client=paddle_client,
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
        transaction_id=transaction_id,
        attempt=attempt,
        retry=retry,
        interval=interval,
    )
