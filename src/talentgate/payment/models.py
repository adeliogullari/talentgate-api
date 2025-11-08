from datetime import datetime

from src.talentgate.database.models import BaseModel


class Invoice(BaseModel):
    transaction_id: str | None = None
    invoice_id: str | None = None
    invoice_number: str | None = None
    total: str | None = None
    currency_code: str | None = None
    status: str | None = None
    billed_at: datetime | None = None


class RetrievedInvoice(BaseModel):
    transaction_id: str | None = None
    invoice_id: str | None = None
    invoice_number: str | None = None
    total: str | None = None
    currency_code: str | None = None
    status: str | None = None
    billed_at: datetime | None = None


class PaddleCheckout(BaseModel):
    name: str
    overview: str | None = None
    jobs: list | None = None
