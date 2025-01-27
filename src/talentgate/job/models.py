from datetime import datetime, UTC
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from src.talentgate.company.models import Company
from src.talentgate.database.models import Observer, BaseModel

if TYPE_CHECKING:
    from src.talentgate.employee.models import Employee
    from src.talentgate.application.models import Application


class LocationType(str, Enum):
    REMOTE = "Remote"
    HYBRID = "Hybrid"
    ONSITE = "Onsite"


class EmploymentType(str, Enum):
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    CONTRACTOR = "Contractor"
    INTERNSHIP = "Internship"


class JobLocation(SQLModel, table=True):
    __tablename__ = "job_location"

    id: int = Field(primary_key=True)
    type: LocationType | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    job: Optional["Job"] = Relationship(back_populates="location")


class JobSalary(SQLModel, table=True):
    __tablename__ = "job_salary"

    id: int = Field(primary_key=True)
    min: str | None = Field(default=None)
    max: str | None = Field(default=None)
    frequency: str | None = Field(default=None)
    job: Optional["Job"] = Relationship(back_populates="salary")


class Job(SQLModel, table=True):
    __tablename__ = "job"

    id: int = Field(primary_key=True)
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    department: str | None = Field(default=None)
    employment_type: EmploymentType | None = Field(default=None)
    job_post_deadline: datetime | None = Field(default=None)
    observers: List["Employee"] = Relationship(
        back_populates="observed_jobs", link_model=Observer
    )
    applications: List["Application"] = Relationship(back_populates="job")
    location_id: int | None = Field(foreign_key="job_location.id", ondelete="CASCADE")
    location: JobLocation | None = Relationship(
        back_populates="job",
        sa_relationship_kwargs={
            "uselist": False,
            "single_parent": True,
            "cascade": "all, delete-orphan",
        },
    )
    salary_id: int | None = Field(foreign_key="job_salary.id")
    salary: JobSalary | None = Relationship(
        back_populates="job", sa_relationship_kwargs={"uselist": False}
    )
    company_id: int | None = Field(foreign_key="company.id")
    company: Company | None = Relationship(
        back_populates="jobs", sa_relationship_kwargs={"uselist": False}
    )
    created_at: datetime | None = Field(default=datetime.now(UTC))
    updated_at: datetime | None = Field(
        default=datetime.now(UTC),
        sa_column_kwargs={"onupdate": datetime.now(UTC)},
    )


class JobLocationRequest(BaseModel):
    type: LocationType | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None


class JobLocationResponse(BaseModel):
    id: int | None = None
    type: LocationType | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None


class CreateJobLocation(JobLocationRequest):
    pass


class CreatedJobLocation(JobLocationResponse):
    pass


class RetrievedJobLocation(JobLocationResponse):
    pass


class UpdateJobLocation(JobLocationRequest):
    pass


class UpdatedJobLocation(JobLocationResponse):
    pass


class DeleteJobLocation(JobLocationRequest):
    pass


class DeletedJobLocation(JobLocationResponse):
    pass


class JobRequest(SQLModel):
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: EmploymentType | None = None
    job_post_deadline: datetime | None = None
    company_id: int | None = None
    location: CreateJobLocation | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class JobResponse(SQLModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: EmploymentType | None = None
    job_post_deadline: datetime | None = None
    company_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class JobQueryParameters(SQLModel):
    offset: int | None = None
    limit: int | None = None
    title: str | None = None


class CreateJob(JobRequest):
    pass


class CreatedJob(JobResponse):
    pass


class RetrievedJob(JobResponse):
    location: JobLocation | None = None


class UpdateJob(JobRequest):
    pass


class UpdatedJob(JobResponse):
    pass


class DeleteJob(JobRequest):
    pass


class DeletedJob(JobResponse):
    pass
