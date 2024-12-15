from enum import Enum
from typing import Optional, TYPE_CHECKING
from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.database.models import BaseModel

if TYPE_CHECKING:
    from src.talentgate.employee.models import Employee


class UserRole(str, Enum):
    ACCOUNT_OWNER = "Account Owner"
    ADMIN = "Admin"


class UserSubscription(str, Enum):
    BASIC = "Basic"
    STANDARD = "Standard"
    PROFESSIONAL = "Professional"
    ENTERPRISE = "Enterprise"


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str = Field(nullable=False)
    verified: bool = Field(default=False)
    image: str | None = Field(default=None)
    role: UserRole | None = Field(default=UserRole.ACCOUNT_OWNER)
    subscription: UserSubscription | None = Field(default=UserSubscription.BASIC)
    employee: Optional["Employee"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
    )


class UserRequest(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    password: str
    verified: bool | None = None
    image: str | None = None
    role: UserRole | None = None
    subscription: UserSubscription | None = None


class UserResponse(BaseModel):
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    verified: bool | None = None
    image: str | None = None
    role: UserRole | None = None
    subscription: UserSubscription | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateUser(UserRequest):
    pass


class CreatedUser(UserResponse):
    pass


class RetrievedUser(UserResponse):
    pass


class UserQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None
    verified: bool | None = None
    role: UserRole | None = None
    subscription: UserSubscription | None = None


class UpdateUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    password: str
    image: str | None = None


class UpdatedUser(UserResponse):
    pass


class DeletedUser(BaseModel):
    id: int
