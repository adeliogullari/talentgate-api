from collections.abc import Sequence
from io import BytesIO
from typing import Annotated

import requests
from fastapi import APIRouter, BackgroundTasks, Depends
from paddle_billing import Client
from pydantic import BaseModel
from sqlmodel import Session
from starlette.responses import RedirectResponse, StreamingResponse

from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.payment import service as payment_service
from src.talentgate.payment.exceptions import CustomerIdNotFoundException
from src.talentgate.payment.models import Invoice, RetrievedInvoice
from src.talentgate.payment.service import get_paddle_client
from src.talentgate.user.models import User
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["payment"])


class PaymentCheckout(BaseModel):
    transaction_id: str | None = None


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
    if not retrieved_user.payment.customer_id:
        raise CustomerIdNotFoundException

    return await payment_service.retrieve_invoices(
        paddle_client=paddle_client, customer_id=retrieved_user.payment.customer_id
    )


@router.get("/api/v1/payment/transactions/{transaction_id}/invoice/document")
def retrieve_invoice_document(
    *, paddle_client: Annotated[Client, Depends(get_paddle_client)], transaction_id: str
) -> StreamingResponse:
    invoice_document = paddle_client.transactions.get_invoice_pdf(transaction_id=transaction_id)

    pdf_response = requests.get(invoice_document.url)
    pdf_bytes = pdf_response.content

    # 2. Wrap in a BytesIO stream
    stream = BytesIO(pdf_bytes)

    # 3. Stream PDF back with correct headers
    headers = {
        "Content-Disposition": f'inline; filename="invoice_{transaction_id}.pdf"'
    }
    return StreamingResponse(stream, media_type="application/pdf", headers=headers)


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
        payment_service.verify_payment,
        paddle_client,
        sqlmodel_session,
        retrieved_user,
        checkout.transaction_id,
    )

    return {
        "transaction_id": checkout.transaction_id,
    }


@router.post("/api/v1/payment/subscription/cancel")
async def cancel_subscription(
    *,
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    background_tasks: BackgroundTasks,
) -> dict[str, str | None]:
    background_tasks.add_task(
        payment_service.cancel_subscription,
        paddle_client,
        sqlmodel_session,
        retrieved_user,
    )

    return {
        "transaction_id": retrieved_user.payment.transaction_id,
        "subscription_id": retrieved_user.payment.subscription_id,
    }
