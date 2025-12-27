from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.database.models import BaseModel
from src.talentgate.user.models import (
    CreatedUser,
    CreateUser,
    RetrievedUser,
    UpdatedUser,
    UpdateUser,
    User,
    UserQueryParameters,
)

if TYPE_CHECKING:
    from src.talentgate.application.models import ApplicationEvaluation
    from src.talentgate.company.models import Company


class Employee(SQLModel, table=True):
    __tablename__ = "employee"

    id: int = Field(primary_key=True)
    title: str | None = Field(default=None)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="employee")
    company_id: int | None = Field(default=None, foreign_key="company.id", ondelete="CASCADE")
    company: Optional["Company"] | None = Relationship(back_populates="employees")
    evaluations: list["ApplicationEvaluation"] = Relationship(back_populates="employee")
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class CreateEmployee(BaseModel):
    title: str | None = None
    user: CreateUser | None = None


class CreatedEmployee(BaseModel):
    id: int
    title: str | None = None
    user: CreatedUser | None = None
    created_at: float
    updated_at: float


class RetrievedEmployee(BaseModel):
    id: int
    title: str | None = None
    user: RetrievedUser | None = None
    created_at: float
    updated_at: float


class EmployeeQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    id: int | None = None
    title: str | None = None
    user: UserQueryParameters | None = None


class UpdateEmployee(BaseModel):
    title: str | None = None
    user: UpdateUser | None = None
    company_id: int | None = None


class UpdatedEmployee(BaseModel):
    id: int
    title: str | None = None
    user: UpdatedUser | None = None
    created_at: float
    updated_at: float


class DeletedEmployee(BaseModel):
    id: int
