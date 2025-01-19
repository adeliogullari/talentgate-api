from enum import StrEnum
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta, UTC
from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.database.models import BaseModel

if TYPE_CHECKING:
    from src.talentgate.user.models import User


class SubscriptionPlan(StrEnum):
    BASIC = "Basic"
    STANDARD = "Standard"


class SubscriptionStatus(StrEnum):
    ACTIVE = "Active"
    EXPIRED = "Expired"


class Subscription(SQLModel, table=True):
    __tablename__ = "subscription"

    id: int = Field(primary_key=True)
    plan: SubscriptionPlan = Field(default=SubscriptionPlan.BASIC)
    start_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC) - timedelta(days=2)
    )
    end_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC) - timedelta(days=1)
    )
    user: Optional["User"] = Relationship(
        back_populates="subscription", sa_relationship_kwargs={"uselist": False}
    )

    @property
    def status(self) -> SubscriptionStatus:
        now = datetime.now(UTC)
        if self.end_date.astimezone() >= now:
            return SubscriptionStatus.ACTIVE
        return SubscriptionStatus.EXPIRED


class CreateSubscription(BaseModel):
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class CreatedSubscription(BaseModel):
    id: int
    plan: SubscriptionPlan
    start_date: datetime
    end_date: datetime
    status: SubscriptionStatus


class RetrievedSubscription(BaseModel):
    id: int
    plan: SubscriptionPlan
    start_date: datetime
    end_date: datetime
    status: SubscriptionStatus


class UpdateSubscription(BaseModel):
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class UpdatedSubscription(BaseModel):
    id: int
    plan: SubscriptionPlan
    start_date: datetime
    end_date: datetime
    status: SubscriptionStatus


class SubscriptionQueryParameters(BaseModel):
    offset: int
    limit: int
    id: int | None = None


class DeletedSubscription(BaseModel):
    id: int
