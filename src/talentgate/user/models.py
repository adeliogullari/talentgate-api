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
    paddle_subscription_id: str | None = Field(default=None)
    plan: str = Field(default=SubscriptionPlan.BASIC.value)
    start_date: float = Field(
        default_factory=lambda: (datetime.now(UTC) - timedelta(minutes=2)).timestamp(),
    )
    end_date: float = Field(
        default_factory=lambda: (datetime.now(UTC) - timedelta(minutes=1)).timestamp(),
    )
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    user: Optional["User"] = Relationship(back_populates="subscription")
    created_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )

    @property
    def status(self) -> SubscriptionStatus:
        now = datetime.now(UTC).timestamp()
        if self.end_date >= now:
            return SubscriptionStatus.ACTIVE
        return SubscriptionStatus.EXPIRED


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
    employee: Optional["Employee"] = Relationship(back_populates="user")
    subscription: UserSubscription | None = Relationship(back_populates="user", cascade_delete=True)
    created_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class CreateSubscription(BaseModel):
    paddle_subscription_id: str | None = None
    plan: str | None = None
    start_date: float | None = None
    end_date: float | None = None


class CreatedSubscription(BaseModel):
    id: int
    paddle_subscription_id: str | None = None
    plan: str
    start_date: float
    end_date: float
    status: str
    created_at: float
    updated_at: float


class RetrievedSubscription(BaseModel):
    id: int
    paddle_subscription_id: str | None = None
    plan: str
    start_date: float
    end_date: float
    status: str
    created_at: float
    updated_at: float


class UpdateSubscription(BaseModel):
    paddle_subscription_id: str | None = None
    plan: str | None = None
    start_date: float | None = None
    end_date: float | None = None


class UpdatedSubscription(BaseModel):
    id: int
    paddle_subscription_id: str | None = None
    plan: str
    start_date: float
    end_date: float
    status: str
    created_at: float
    updated_at: float


class CreateUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    verified: bool | None = None
    role: str | None = None
    subscription: CreateSubscription | None = None


class CreatedUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: CreatedSubscription | None = None
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
    subscription: UpdateSubscription | None = None


class UpdatedUser(BaseModel):
    id: int | None = None
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: UpdatedSubscription | None = None
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
    subscription: UpdatedSubscription | None = None
    created_at: float
    updated_at: float


class DeletedUser(BaseModel):
    id: int


class DeletedCurrentUser(BaseModel):
    id: int
