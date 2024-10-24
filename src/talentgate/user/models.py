from enum import Enum
from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class UserRole(str, Enum):
    ACCOUNT_OWNER = "account_owner"
    ADMIN = "admin"
    SUPERADMIN = "super_admin"


class UserSubscription(str, Enum):
    FREE = "free"
    STANDARD = "standard"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


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
    subscription: UserSubscription | None = Field(default=UserSubscription.FREE)


class UserRequest(SQLModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    password: str
    verified: bool | None = None
    role: UserRole | None = None
    image: str | None = None
    subscription: UserSubscription | None = None


class UserResponse(SQLModel):
    id: int | None
    firstname: str | None
    lastname: str | None
    username: str
    email: str
    verified: bool | None
    role: UserRole | None
    image: str | None
    subscription: UserSubscription | None = None


class CreateUser(UserRequest):
    pass


class CreatedUser(UserResponse):
    pass


class RetrievedUser(UserResponse):
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
    subscription: UserSubscription | None = None


class UpdateUser(UserRequest):
    pass

class UpdatedUser(UserResponse):
    pass

class DeletedUser(SQLModel):
    id: int