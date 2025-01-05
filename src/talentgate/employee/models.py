from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Any
from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.job.models import Job
from src.talentgate.database.models import BaseModel, Observer
from src.talentgate.user.models import User, UserRole

if TYPE_CHECKING:
    from src.talentgate.application.models import ApplicationEvaluation


class EmployeeTitle(str, Enum):
    FOUNDER = "Founder"
    RECRUITER = "Recruiter"
    INITIATE = "Initiate"


class Employee(SQLModel, table=True):
    __tablename__ = "employee"

    id: int = Field(primary_key=True)
    title: EmployeeTitle | None = Field(default=EmployeeTitle.INITIATE)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="employee")
    application_evaluations: List["ApplicationEvaluation"] = Relationship(
        back_populates="employee"
    )
    observed_jobs: List["Job"] = Relationship(
        back_populates="observers", link_model=Observer
    )


User.model_rebuild()


class EmployeeRequest(BaseModel):
    title: EmployeeTitle | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    password: str
    verified: bool | None = None
    image: str | None = None


class EmployeeResponse(SQLModel):
    id: int | None = None
    title: EmployeeTitle | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    verified: bool | None = None
    image: str | None = None
    role: UserRole | None = None
    subscription: Any | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateEmployee(EmployeeRequest):
    pass


class CreatedEmployee(EmployeeResponse):
    pass


class RetrievedEmployee(EmployeeResponse):
    pass


class EmployeeQueryParameters(SQLModel):
    offset: int | None = None
    limit: int | None = None
    title: EmployeeTitle | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    verified: bool | None = None
    image: str | None = None
    role: UserRole | None = None
    subscription: Any | None = None


class UpdateEmployee(EmployeeRequest):
    pass


class UpdatedEmployee(EmployeeResponse):
    pass


class DeletedEmployee(SQLModel):
    id: int
