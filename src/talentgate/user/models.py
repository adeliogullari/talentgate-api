from enum import Enum
from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class UserRole(str, Enum):
    ACCOUNT_OWNER = "account_owner"
    ADMIN = "admin"
    SUPERADMIN = "super_admin"


class UserSubscriptionType(str, Enum):
    STANDARD = "standard"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class UserSubscriptionPlanName(str, Enum):
    STANDARD = "standard"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class UserSubscriptionPlan(SQLModel, table=True):
    __tablename__ = "user_subscription_plan"
    id: int = Field(primary_key=True)
    name: UserSubscriptionPlanName = Field(unique=True)
    price: str = Field(gt=0)
    billing_cycle: str = Field(default="monthly")


class UserSubscription(SQLModel, table=True):
    __tablename__ = "user_subscription"

    id: int = Field(primary_key=True)
    type: UserSubscriptionType | None = Field(default=UserSubscriptionType.STANDARD)
    start_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_date: datetime | None = Field(default=None)


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: bytes = Field(nullable=False)
    verified: bool = Field(default=False)
    role: UserRole | None = Field(default=UserRole.ACCOUNT_OWNER)
    image: str | None = Field(default=None)
    # subscription: UserSubscription | None = Relationship(
    #     back_populates="user", sa_relationship_kwargs={"uselist": False}
    # )


class UserRequest(SQLModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    password: str
    verified: bool | None = None
    role: UserRole | None = None
    image: str | None = None


class UserResponse(SQLModel):
    id: int | None
    firstname: str | None
    lastname: str | None
    username: str
    email: str
    verified: bool | None
    role: UserRole | None
    image: str | None


class CreateUserRequest(UserRequest):
    pass


class CreateUserResponse(UserResponse):
    pass


class RetrieveUserResponse(UserResponse):
    pass


class UserQueryParameters(SQLModel):
    offset: int | None = Field(100, gt=0, le=100)
    limit: int | None = Field(0, ge=0)
    firstname: str | None
    lastname: str | None
    username: str | None = None
    email: str | None = None
    verified: bool | None = None
    role: UserRole | None = None


class UpdateUserRequest(UserRequest):
    pass


class UpdateUserResponse(UserResponse):
    pass


class DeleteUserRequest(SQLModel):
    id: str


class DeleteUserResponse(UserResponse):
    pass
