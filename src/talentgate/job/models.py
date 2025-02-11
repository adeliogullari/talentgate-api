from datetime import datetime, UTC
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from src.talentgate.company.models import Company
from src.talentgate.database.models import Observer, BaseModel

if TYPE_CHECKING:
    from src.talentgate.employee.models import Employee
    from src.talentgate.application.models import Application


class JobLocationType(str, Enum):
    REMOTE = "Remote"
    HYBRID = "Hybrid"
    ONSITE = "Onsite"


class EmploymentType(str, Enum):
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    CONTRACTOR = "Contractor"
    INTERNSHIP = "Internship"


class JobAddress(SQLModel, table=True):
    __tablename__ = "job_address"

    id: int = Field(primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    location: Optional["JobLocation"] = Relationship(
        back_populates="address",
        sa_relationship_kwargs={"uselist": False},
    )


class JobLocation(SQLModel, table=True):
    __tablename__ = "job_location"

    id: int = Field(primary_key=True)
    type: JobLocationType | None = Field(default=JobLocationType.ONSITE)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    address_id: int | None = Field(default=None, foreign_key="job_address.id")
    address: Optional[JobAddress] = Relationship(back_populates="location")
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
        back_populates="observations", link_model=Observer
    )
    applications: List["Application"] = Relationship(back_populates="job")
    location_id: int | None = Field(foreign_key="job_location.id", ondelete="CASCADE")
    location: JobLocation | None = Relationship(
        back_populates="job",
        sa_relationship_kwargs={
            "uselist": False,
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


class CreateAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreatedAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class RetrievedAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdateAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdatedAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateLocation(BaseModel):
    type: JobLocationType | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateAddress | None = None


class CreatedLocation(BaseModel):
    id: int
    type: JobLocationType | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateAddress | None = None


class RetrievedLocation(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdateLocation(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdatedLocation(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class JobRequest(SQLModel):
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: EmploymentType | None = None
    job_post_deadline: datetime | None = None
    company_id: int | None = None
    location: CreateLocation | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class JobResponse(SQLModel):
    id: int | None = None
    title: str | None = None
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
    employment_type: List[EmploymentType] | None = None
    location_type: List[JobLocationType] | None = None
    department: List[str] | None = None


class CreateJob(JobRequest):
    pass


class CreatedJob(JobResponse):
    pass


class RetrievedJob(JobResponse):
    description: str | None = None
    location: RetrievedLocation | None = None


class RetrievedCompanyJob(RetrievedJob):
    pass


class RetrievedCompanyJobs(JobResponse):
    location: RetrievedLocation | None = None


class UpdateJob(JobRequest):
    pass


class UpdatedJob(JobResponse):
    pass


class DeleteJob(JobRequest):
    pass


class DeletedJob(JobResponse):
    pass
