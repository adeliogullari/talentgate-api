from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from paddle_billing import Client
from pydantic import BaseModel
from sqlmodel import Session

from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.payment import service as payment_service
from src.talentgate.payment.service import get_paddle_client
from src.talentgate.user.models import User
from src.talentgate.user.views import retrieve_current_user

router = APIRouter(tags=["payment"])


class PaymentCheckout(BaseModel):
    transaction_id: str | None = None


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
