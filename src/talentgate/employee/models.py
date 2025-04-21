from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.company.models import Company
from src.talentgate.database.models import BaseModel, Observer
from src.talentgate.user.models import (
    CreatedUser,
    CreateUser,
    RetrievedUser,
    UpdatedUser,
    UpdateUser,
    User,
    UserRole,
    UserSubscription,
)

if TYPE_CHECKING:
    from src.talentgate.application.models import ApplicationEvaluation
    from src.talentgate.job.models import Job


class Employee(SQLModel, table=True):
    __tablename__ = "employee"

    id: int = Field(primary_key=True)
    title: str | None = Field(default=None)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="employee")
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: Company | None = Relationship(back_populates="employees")
    evaluations: list["ApplicationEvaluation"] = Relationship(back_populates="employee")
    observations: list["Job"] = Relationship(
        back_populates="observers",
        link_model=Observer,
    )
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class EmployeeUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: UserRole | None = None
    subscription: UserSubscription | None = None
    created_at: datetime
    updated_at: datetime


class EmployeeCompany(BaseModel):
    id: int | None = None
    name: str | None = None
    overview: str | None = None


class CreateEmployee(BaseModel):
    id: int | None = None
    title: str | None = None
    user: CreateUser | None = None


class CreatedEmployee(BaseModel):
    id: int
    title: str | None = None
    user: CreatedUser | None = None
    company: EmployeeCompany | None = None
    created_at: float
    updated_at: float


class RetrievedEmployee(BaseModel):
    id: int
    title: str | None = None
    user: RetrievedUser | None = None
    company: EmployeeCompany | None = None
    created_at: float
    updated_at: float


class EmployeeQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    id: int | None = None
    title: str | None = None


class UpdateEmployee(BaseModel):
    id: int | None = None
    title: str | None = None
    user: UpdateUser | None = None


class UpdatedEmployee(BaseModel):
    id: int
    title: str | None = None
    user: UpdatedUser | None = None
    company: EmployeeCompany | None = None
    created_at: float
    updated_at: float


class DeletedEmployee(BaseModel):
    id: int
