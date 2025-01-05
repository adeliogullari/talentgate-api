from enum import Enum
from datetime import datetime, timedelta, UTC
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.database.models import BaseModel


class SubscriptionPlan(str, Enum):
    BASIC = "Basic"
    STANDARD = "Standard"


class SubscriptionStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"


class Subscription(SQLModel, table=True):
    __tablename__ = "subscription"

    id: int = Field(primary_key=True)
    plan: SubscriptionPlan = Field(default=SubscriptionPlan.BASIC)
    start_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC) - timedelta(days=1)
    )
    user: Optional["User"] = Relationship(
        back_populates="subscription", sa_relationship_kwargs={"uselist": False}
    )


class CreateSubscription(BaseModel):
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class CreatedSubscription(BaseModel):
    id: int | None = None
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: SubscriptionStatus | None = None


class RetrievedSubscription(BaseModel):
    id: int | None = None
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: SubscriptionStatus | None = None


class UpdateSubscription(BaseModel):
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class UpdatedSubscription(BaseModel):
    id: int | None = None
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: SubscriptionStatus | None = None


class SubscriptionQueryParameters(BaseModel):
    offset: int
    limit: int
    id: int | None = None
    status: SubscriptionStatus | None = None


class DeletedSubscription(BaseModel):
    id: int
