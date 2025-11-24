import asyncio
from datetime import UTC, timedelta

from paddle_billing import Client, Environment, Options
from paddle_billing.Entities.Shared import (
    PaymentAttemptStatus,
    TransactionStatus,
)
from paddle_billing.Entities.Subscription import Subscription
from paddle_billing.Entities.Subscriptions import (
    SubscriptionEffectiveFrom,
    SubscriptionItemStatus,
    SubscriptionStatus,
)
from paddle_billing.Entities.Transaction import Transaction
from paddle_billing.Resources.Products.Operations import ListProducts, ProductIncludes
from paddle_billing.Resources.Subscriptions.Operations import CancelSubscription
from paddle_billing.Resources.Transactions.Operations import ListTransactions
from sqlmodel import Session

from config import get_settings
from src.talentgate.payment.models import (
    Invoice,
    RetrievedPrice,
    RetrievedProduct,
    RetrievedSubscription,
    RetrievedUnitPrice,
)
from src.talentgate.user import service as user_service
from src.talentgate.user.models import UpdateSubscription, User

settings = get_settings()


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


async def retrieve_subscription(
    paddle_client: Client,
    retrieved_user: User,
) -> RetrievedSubscription:
    next_billing_date = None
    amount = None

    if retrieved_user.subscription.paddle_subscription_id:
        subscription = paddle_client.subscriptions.get(
            subscription_id=retrieved_user.subscription.paddle_subscription_id
        )
        next_billing_date = subscription.next_billed_at.timestamp()

        price = str(int(subscription.items[0].price.unit_price.amount) // 100)
        currency_code = subscription.currency_code.value
        billing_cycle = subscription.billing_cycle.interval.value

        amount = f"{price} {currency_code} / {billing_cycle}"

    return RetrievedSubscription(
        plan=retrieved_user.subscription.plan,
        status=retrieved_user.subscription.status,
        start_date=retrieved_user.subscription.start_date,
        end_date=retrieved_user.subscription.end_date,
        next_billing_date=next_billing_date,
        amount=amount,
    )


async def retrieve_products(
    paddle_client: Client,
) -> list[RetrievedProduct]:
    products = paddle_client.products.list(
        operation=ListProducts(
            ids=[
                settings.paddle_standard_plan_product_id,
                settings.paddle_premium_plan_product_id,
            ],
            includes=[ProductIncludes.Prices],
        )
    )

    return list(
        reversed(
            [
                RetrievedProduct(
                    id=product.id,
                    name=product.name.lower(),
                    description=product.description,
                    prices=[
                        RetrievedPrice(
                            id=price.id,
                            billing_cycle=price.billing_cycle.interval.name.lower(),
                            unit_price=RetrievedUnitPrice(
                                amount=str(int(price.unit_price.amount) // 100),
                                currency_code=price.unit_price.currency_code.value.lower(),
                            ),
                        )
                        for price in product.prices
                    ],
                )
                for product in products
            ]
        )
    )


async def update_subscription(
    sqlmodel_session: Session,
    subscription: Subscription,
    retrieved_user: User,
) -> None:
    plan = subscription.items[0].product.name.lower()
    start_date = subscription.current_billing_period.starts_at.replace(
        tzinfo=UTC
    ).timestamp()
    end_date = (
        subscription.current_billing_period.ends_at.replace(tzinfo=UTC)
        + timedelta(days=3)
    ).timestamp()

    await user_service.update_subscription(
        sqlmodel_session=sqlmodel_session,
        retrieved_subscription=retrieved_user.subscription,
        subscription=UpdateSubscription(
            paddle_subscription_id=subscription.id,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
        ),
    )


async def sync_subscription(
    paddle_client: Client, sqlmodel_session: Session, retrieved_user: User
) -> None:
    subscription = paddle_client.subscriptions.get(
        subscription_id=retrieved_user.subscription.paddle_subscription_id
    )

    await update_subscription(
        sqlmodel_session=sqlmodel_session,
        subscription=subscription,
        retrieved_user=retrieved_user,
    )


async def cancel_subscription(
    paddle_client: Client, sqlmodel_session: Session, retrieved_user: User
) -> None:
    paddle_client.subscriptions.cancel(
        subscription_id=retrieved_user.subscription.paddle_subscription_id,
        operation=CancelSubscription(
            effective_from=SubscriptionEffectiveFrom("next_billing_period")
        ),
    )

    await user_service.update_subscription(
        sqlmodel_session=sqlmodel_session,
        retrieved_subscription=retrieved_user.subscription,
        subscription=UpdateSubscription(
            paddle_subscription_id=None,
        ),
    )


async def retrieve_invoices(
    paddle_client: Client, retrieved_user: User
) -> list[Invoice] | None:
    transactions = paddle_client.transactions.list(
        operation=ListTransactions(
            subscription_ids=[retrieved_user.subscription.paddle_subscription_id]
        )
    )

    return [
        Invoice(
            transaction_id=transaction.id,
            invoice_id=transaction.invoice_id,
            invoice_number=transaction.invoice_number,
            total=str(int(transaction.details.totals.total) // 100),
            currency_code=transaction.details.totals.currency_code.value,
            status=transaction.status.value,
            billed_at=transaction.billed_at,
            card_type=transaction.payments[0].method_details.card.type.value,
            card_last4=transaction.payments[0].method_details.card.last4,
        )
        for transaction in transactions
    ]


async def retrieve_invoice_document(paddle_client: Client, transaction_id: str) -> None:
    return paddle_client.transactions.get_invoice_pdf(transaction_id=transaction_id)


async def confirm_transaction(
    paddle_client: Client,
    sqlmodel_session: Session,
    retrieved_user: User,
    transaction_id: str,
    attempt: int = 0,
    retry: int = 5,
    interval: float = 5,
) -> bool:
    await asyncio.sleep(interval)

    transaction = paddle_client.transactions.get(transaction_id=transaction_id)
    subscription = paddle_client.subscriptions.get(
        subscription_id=transaction.subscription_id
    )

    is_transaction_verified = await verify_transaction(transaction=transaction)
    is_subscription_verified = await verify_subscription(subscription=subscription)

    if is_transaction_verified and is_subscription_verified:
        if retrieved_user.subscription.paddle_subscription_id:
            await cancel_subscription(
                paddle_client=paddle_client,
                sqlmodel_session=sqlmodel_session,
                retrieved_user=retrieved_user,
            )

        await update_subscription(
            sqlmodel_session=sqlmodel_session,
            subscription=subscription,
            retrieved_user=retrieved_user,
        )

        return True

    if attempt >= retry:
        return False

    attempt += 1

    return await confirm_transaction(
        paddle_client=paddle_client,
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
        transaction_id=transaction_id,
        attempt=attempt,
        retry=retry,
        interval=interval,
    )
