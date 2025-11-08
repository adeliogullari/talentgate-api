from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.database.models import BaseModel
from src.talentgate.user.enums import SubscriptionPlan, SubscriptionStatus, UserRole

if TYPE_CHECKING:
    from src.talentgate.employee.models import Employee


class UserSubscription(SQLModel, table=True):
    __tablename__ = "user_subscription"

    id: int = Field(primary_key=True)
    plan: str = Field(default=SubscriptionPlan.BASIC.value)
    start_date: float = Field(
        default_factory=lambda: (datetime.now(UTC) - timedelta(days=2)).timestamp(),
    )
    end_date: float = Field(
        default_factory=lambda: (datetime.now(UTC) - timedelta(days=1)).timestamp(),
    )
    user: Optional["User"] = Relationship(back_populates="subscription")

    @property
    def status(self) -> SubscriptionStatus:
        now = datetime.now(UTC).timestamp()
        if self.end_date >= now:
            return SubscriptionStatus.ACTIVE
        return SubscriptionStatus.EXPIRED


class UserPayment(SQLModel, table=True):
    __tablename__ = "user_payment"

    id: int = Field(primary_key=True)
    customer_id: str | None = Field(default=None)
    transaction_id: str | None = Field(default=None)
    subscription_id: str | None = Field(default=None)
    user: Optional["User"] = Relationship(back_populates="payment")
    start_date: float = Field(
        default_factory=lambda: (datetime.now(UTC) - timedelta(days=2)).timestamp(),
    )
    end_date: float = Field(
        default_factory=lambda: (datetime.now(UTC) - timedelta(days=1)).timestamp(),
    )


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str = Field(nullable=False)
    profile: str | None = Field(default=None)
    verified: bool = Field(default=False)
    role: str = Field(default=UserRole.OWNER.value)
    employee: Optional["Employee"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "cascade": "all"},
    )
    subscription_id: int | None = Field(
        default=None,
        foreign_key="user_subscription.id",
    )
    subscription: UserSubscription | None = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "cascade": "all"},
    )
    payment_id: int | None = Field(
        default=None,
        foreign_key="user_payment.id",
    )
    payment: UserPayment | None = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "cascade": "all"},
    )
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class CreateSubscription(BaseModel):
    plan: str | None = None
    start_date: float | None = None
    end_date: float | None = None


class CreatedSubscription(BaseModel):
    id: int
    plan: str
    start_date: float
    end_date: float
    status: str


class RetrievedSubscription(BaseModel):
    id: int
    plan: str
    start_date: float
    end_date: float
    status: str


class UpdateSubscription(BaseModel):
    plan: str | None = None
    start_date: float | None = None
    end_date: float | None = None


class UpdatedSubscription(BaseModel):
    id: int
    plan: str
    start_date: float
    end_date: float
    status: str


class UpsertSubscription(BaseModel):
    id: int
    plan: str | None = None
    start_date: float | None = None
    end_date: float | None = None


class UpsertedSubscription(BaseModel):
    id: int
    plan: str
    start_date: float
    end_date: float
    status: str


class CreatePayment(BaseModel):
    customer_id: str | None = None
    transaction_id: str | None = None
    subscription_id: str | None = None


class CreatedPayment(BaseModel):
    id: int
    customer_id: str | None = None
    transaction_id: str | None = None
    subscription_id: str | None = None


class RetrievedPayment(BaseModel):
    id: int
    customer_id: str | None = None
    transaction_id: str | None = None
    subscription_id: str | None = None


class UpdatePayment(BaseModel):
    customer_id: str | None = None
    transaction_id: str | None = None
    subscription_id: str | None = None


class UpdatedPayment(BaseModel):
    id: int
    customer_id: str | None = None
    transaction_id: str | None = None
    subscription_id: str | None = None


class UpsertPayment(BaseModel):
    id: int
    customer_id: str | None = None
    transaction_id: str | None = None
    subscription_id: str | None = None


class UpsertedPayment(BaseModel):
    id: int
    customer_id: str | None = None
    transaction_id: str | None = None
    subscription_id: str | None = None


class CreateUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    verified: bool | None = None
    role: str | None = None
    subscription_id: int | None = None
    subscription: UpsertSubscription | None = None
    payment_id: int | None = None


class CreatedUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: UpsertedSubscription | None = None
    created_at: float
    updated_at: float


class RetrievedUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: RetrievedSubscription | None = None
    created_at: float
    updated_at: float


class RetrievedCurrentUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: RetrievedSubscription | None = None
    created_at: float
    updated_at: float


class UserQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None
    verified: bool | None = None
    role: str | None = None


class UpdateUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None
    verified: bool | None = None
    role: str | None = None
    profile: str | None = None
    subscription_id: int | None = None
    subscription: UpsertSubscription | None = None


class UpdatedUser(BaseModel):
    id: int | None = None
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: UpsertedSubscription | None = None
    created_at: float
    updated_at: float


class UpsertUser(BaseModel):
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None
    verified: bool | None = None
    role: str | None = None
    subscription_id: int | None = None
    subscription: UpsertSubscription | None = None


class UpsertedUser(BaseModel):
    id: int | None = None
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: UpsertedSubscription | None = None
    created_at: float
    updated_at: float


class UpdateCurrentUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None
    profile: str | None = None


class UpdatedCurrentUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: UpsertedSubscription | None = None
    created_at: float
    updated_at: float


class DeletedUser(BaseModel):
    id: int


class DeletedCurrentUser(BaseModel):
    id: int
