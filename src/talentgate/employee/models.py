from enum import StrEnum
from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.job.models import Job
from src.talentgate.database.models import BaseModel, Observer
from src.talentgate.user.models import User, UserRole, UserSubscription


if TYPE_CHECKING:
    from src.talentgate.application.models import ApplicationEvaluation


class EmployeeTitle(StrEnum):
    FOUNDER = "Founder"
    RECRUITER = "Recruiter"


class Employee(SQLModel, table=True):
    __tablename__ = "employee"

    id: int = Field(primary_key=True)
    title: EmployeeTitle | None = Field(default=None)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="employee")
    application_evaluations: List["ApplicationEvaluation"] = Relationship(
        back_populates="employee"
    )
    observed_jobs: List["Job"] = Relationship(
        back_populates="observers", link_model=Observer
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


class CreateEmployee(BaseModel):
    title: EmployeeTitle | None = None
    user_id: int | None = None


class CreatedEmployee(BaseModel):
    id: int
    title: EmployeeTitle | None = None
    user: EmployeeUser | None = None


class RetrievedEmployee(BaseModel):
    id: int
    title: EmployeeTitle | None = None
    user: EmployeeUser | None = None


class EmployeeQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    id: int | None = None
    title: EmployeeTitle | None = None


class UpdateEmployee(BaseModel):
    title: EmployeeTitle | None = None
    user_id: int | None = None


class UpdatedEmployee(BaseModel):
    id: int
    title: EmployeeTitle | None = None
    user: EmployeeUser | None = None


class DeletedEmployee(BaseModel):
    id: int
