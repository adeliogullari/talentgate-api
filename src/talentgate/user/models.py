from enum import Enum
from datetime import datetime, timedelta, UTC
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.database.models import BaseModel

if TYPE_CHECKING:
    from src.talentgate.employee.models import Employee


class UserRole(str, Enum):
    ACCOUNT_OWNER = "Account Owner"
    ADMIN = "Admin"


class SubscriptionPlan(str, Enum):
    BASIC = "Basic"
    STANDARD = "Standard"


class SubscriptionStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"


class UserSubscription(SQLModel, table=True):
    __tablename__ = "user_subscription"

    id: int = Field(primary_key=True)
    plan: SubscriptionPlan = Field(default=SubscriptionPlan.BASIC)
    start_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC) - timedelta(days=1)
    )
    user: Optional["User"] = Relationship(
        back_populates="subscription", sa_relationship_kwargs={"uselist": False}
    )

    @property
    def status(self) -> str:
        if self.end_date > datetime.now(UTC):
            return SubscriptionStatus.ACTIVE
        else:
            return SubscriptionStatus.EXPIRED


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str = Field(nullable=False)
    verified: bool = Field(default=False)
    role: UserRole | None = Field(default=UserRole.ACCOUNT_OWNER)
    employee: Optional["Employee"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "cascade": "all"},
    )
    subscription_id: int | None = Field(
        default=None, foreign_key="user_subscription.id"
    )
    subscription: Optional["UserSubscription"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "cascade": "all"},
    )
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
    )


class CreateUserSubscription(BaseModel):
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class Subscription(BaseModel):
    id: int | None = None
    plan: SubscriptionPlan | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: SubscriptionStatus | None = None


class CreateUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    verified: bool | None = None
    role: UserRole | None = None
    subscription: Subscription | None = None
    subscription_id: int | None = None


class CreatedUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: UserRole
    subscription: Subscription | None = None
    created_at: datetime
    updated_at: datetime


class RetrievedUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: UserRole
    subscription: Subscription | None = None
    created_at: datetime
    updated_at: datetime


class RetrievedCurrentUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: UserRole
    subscription: Subscription | None = None
    created_at: datetime
    updated_at: datetime


class UserQueryParameters(BaseModel):
    offset: int
    limit: int
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None
    verified: bool | None = None
    role: UserRole | None = None


class UpdateUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None
    verified: bool | None = None
    role: UserRole | None = None
    subscription: Subscription | None = None
    subscription_id: int | None = None


class UpdatedUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: UserRole
    subscription: Subscription | None = None
    created_at: datetime
    updated_at: datetime


class UpdateCurrentUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None


class UpdatedCurrentUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class DeletedUser(BaseModel):
    id: int


class DeletedCurrentUser(BaseModel):
    id: int
