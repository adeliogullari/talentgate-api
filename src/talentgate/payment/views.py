from collections.abc import Sequence
from io import BytesIO
from typing import Annotated

import requests
from fastapi import APIRouter, BackgroundTasks, Depends
from paddle_billing import Client
from sqlmodel import Session
from starlette.responses import StreamingResponse

from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.payment import service as payment_service
from src.talentgate.payment.exceptions import UserSubscriptionNotFoundException
from src.talentgate.payment.models import (
    Invoice,
    PaymentCheckout,
    RetrievedInvoice,
    RetrievedProduct,
    RetrievedSubscription,
)
from src.talentgate.payment.service import get_paddle_client
from src.talentgate.user.models import User
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["payment"])


@router.post("/api/v1/payment/checkout")
async def payment_checkout(
    *,
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    background_tasks: BackgroundTasks,
    checkout: PaymentCheckout,
) -> dict[str, str | None]:
    background_tasks.add_task(
        payment_service.confirm_transaction,
        paddle_client,
        sqlmodel_session,
        retrieved_user,
        checkout.transaction_id,
    )

    return {
        "transaction_id": checkout.transaction_id,
    }


@router.get("/api/v1/payment/subscription")
async def retrieve_subscription(
    *,
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
) -> RetrievedSubscription:
    return await payment_service.retrieve_subscription(
        paddle_client=paddle_client, retrieved_user=retrieved_user
    )


@router.get("/api/v1/payment/products")
async def retrieve_products(
    *,
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
) -> list[RetrievedProduct]:
    return await payment_service.retrieve_products(paddle_client=paddle_client)


@router.post("/api/v1/payment/subscription/cancel")
async def cancel_subscription(
    *,
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    background_tasks: BackgroundTasks,
) -> dict[str, str | None]:
    if not retrieved_user.subscription.paddle_subscription_id:
        raise UserSubscriptionNotFoundException

    background_tasks.add_task(
        payment_service.cancel_subscription,
        paddle_client,
        retrieved_user,
    )

    return {
        "subscription_id": retrieved_user.subscription.paddle_subscription_id,
    }


@router.get(
    path="/api/v1/payment/invoices",
    response_model=list[RetrievedInvoice],
    status_code=200,
)
async def retrieve_invoices(
    *,
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
) -> Sequence[Invoice]:
    if not retrieved_user.subscription.paddle_subscription_id:
        raise UserSubscriptionNotFoundException

    return await payment_service.retrieve_invoices(
        paddle_client=paddle_client, retrieved_user=retrieved_user
    )


@router.get("/api/v1/payment/transactions/{transaction_id}/invoice/document")
def retrieve_invoice_document(
    *, paddle_client: Annotated[Client, Depends(get_paddle_client)], transaction_id: str
) -> StreamingResponse:
    invoice_document = paddle_client.transactions.get_invoice_pdf(
        transaction_id=transaction_id
    )

    pdf_response = requests.get(invoice_document.url, timeout=10)
    pdf_bytes = pdf_response.content

    stream = BytesIO(pdf_bytes)

    headers = {
        "Content-Disposition": f'inline; filename="invoice_{transaction_id}.pdf"'
    }
    return StreamingResponse(stream, media_type="application/pdf", headers=headers)
