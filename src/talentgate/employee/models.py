from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

from src.talentgate.job.models import Job
from src.talentgate.link.models import Observer
from src.talentgate.user.models import User

if TYPE_CHECKING:
    from src.talentgate.application.models import ApplicationEvaluation


class EmployeeTitle(str, Enum):
    FOUNDER = "founder"
    RECRUITER = "recruiter"


class EmploymentType(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class Employee(SQLModel, table=True):
    __tablename__ = "employee"

    id: int = Field(primary_key=True)
    title: EmployeeTitle | None = Field(default=None)
    salary: str | None = Field(default=None)
    user_id: int | None = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="employee")
    application_evaluations: List["ApplicationEvaluation"] = Relationship(
        back_populates="employee"
    )
    observed_jobs: List["Job"] = Relationship(
        back_populates="observers", link_model=Observer
    )


User.model_rebuild()


class EmployeeRequest(SQLModel):
    title: EmployeeTitle | None = None
    salary: str | None = None


class EmployeeResponse(SQLModel):
    id: int | None = None
    title: EmployeeTitle | None = None
    salary: str | None = None


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
    salary: str | None = None


class UpdateEmployee(EmployeeRequest):
    pass


class UpdatedEmployee(EmployeeResponse):
    pass


class DeletedEmployee(SQLModel):
    id: int
