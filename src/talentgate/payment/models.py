from datetime import datetime

from src.talentgate.database.models import BaseModel


class PaymentCheckout(BaseModel):
    transaction_id: str | None = None


class RetrievedSubscription(BaseModel):
    plan: str | None = None
    status: str | None = None
    start_date: float | None = None
    end_date: float | None = None
    next_billing_date: float | None = None
    amount: str | None = None


class RetrievedUnitPrice(BaseModel):
    amount: str | None = None
    currency_code: str | None = None


class RetrievedPrice(BaseModel):
    id: str | None = None
    billing_cycle: str | None = None
    unit_price: RetrievedUnitPrice | None = None


class RetrievedProduct(BaseModel):
    id: str | None = None
    name: str | None = None
    description: str | None = None
    prices: list[RetrievedPrice] | None = None


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
