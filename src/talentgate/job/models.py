from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.database.models import BaseModel

if TYPE_CHECKING:
    from src.talentgate.application.models import Application
    from src.talentgate.company.models import Company


class JobLocationAddress(SQLModel, table=True):
    __tablename__ = "job_location_address"

    id: int | None = Field(default=None, primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    location_id: int | None = Field(default=None, foreign_key="job_location.id", ondelete="CASCADE")
    location: Optional["JobLocation"] = Relationship(back_populates="address")


class JobLocation(SQLModel, table=True):
    __tablename__ = "job_location"

    id: int | None = Field(default=None, primary_key=True)
    type: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    address: JobLocationAddress | None = Relationship(back_populates="location", cascade_delete=True)
    job_id: int | None = Field(default=None, foreign_key="job.id", ondelete="CASCADE")
    job: Optional["Job"] = Relationship(back_populates="location")


class JobSalary(SQLModel, table=True):
    __tablename__ = "job_salary"

    id: int | None = Field(default=None, primary_key=True)
    min: float | None = Field(default=None, ge=0)
    max: float | None = Field(default=None, ge=0)
    frequency: str | None = Field(default=None)
    currency: str | None = Field(default=None)
    job_id: int | None = Field(default=None, foreign_key="job.id", ondelete="CASCADE")
    job: Optional["Job"] = Relationship(back_populates="salary")


class Job(SQLModel, table=True):
    __tablename__ = "job"

    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    department: str | None = Field(default=None)
    employment_type: str | None = Field(default=None)
    applications: list["Application"] = Relationship(back_populates="job", cascade_delete=True)
    location: JobLocation | None = Relationship(
        back_populates="job",
        cascade_delete=True,
    )
    salary: JobSalary | None = Relationship(
        back_populates="job",
        cascade_delete=True,
    )
    company_id: int | None = Field(default=None, foreign_key="company.id", ondelete="CASCADE")
    company: Optional["Company"] = Relationship(back_populates="jobs")
    created_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class CreateJobLocationAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreatedJobLocationAddress(BaseModel):
    id: int | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class RetrievedJobLocationAddress(BaseModel):
    id: int | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdateJobLocationAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdatedJobLocationAddress(BaseModel):
    id: int | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateJobLocation(BaseModel):
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateJobLocationAddress | None = None


class CreatedJobLocation(BaseModel):
    id: int | None = None
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateJobLocationAddress | None = None


class RetrievedJobLocation(BaseModel):
    id: int | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdateJobLocation(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdatedJobLocation(BaseModel):
    id: int | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateSalary(BaseModel):
    min: float | None = None
    max: float | None = None
    frequency: str | None = None
    currency: str | None = None


class CreatedSalary(BaseModel):
    id: int | None = None
    min: float | None = None
    max: float | None = None
    frequency: str | None = None
    currency: str | None = None


class RetrievedJobSalary(BaseModel):
    id: int | None = None
    min: float | None = None
    max: float | None = None
    frequency: str | None = None
    currency: str | None = None


class UpdateSalary(BaseModel):
    min: float | None = None
    max: float | None = None
    frequency: str | None = None
    currency: str | None = None


class UpdatedSalary(BaseModel):
    id: int | None = None
    min: float | None = None
    max: float | None = None
    frequency: str | None = None
    currency: str | None = None


class JobQueryParameters(SQLModel):
    offset: int | None = None
    limit: int | None = None
    title: str | None = None
    department: str | None = None
    employment_type: str | None = None


class CreateJob(BaseModel):
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: str | None = None
    location: CreateJobLocation | None = None
    salary: CreateSalary | None = None


class CreatedJob(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: str | None = None
    location: CreateJobLocation | None = None
    salary: CreateSalary | None = None
    created_at: float | None = None
    updated_at: float | None = None


class RetrievedJob(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: str | None = None
    location: CreateJobLocation | None = None
    salary: CreateSalary | None = None
    created_at: float | None = None
    updated_at: float | None = None


class UpdateJob(BaseModel):
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: str | None = None
    location: UpdateJobLocation | None = None
    salary: UpdateSalary | None = None
    created_at: float | None = None
    updated_at: float | None = None


class UpdatedJob(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: str | None = None
    location: CreateJobLocation | None = None
    salary: CreateSalary | None = None
    created_at: float | None = None
    updated_at: float | None = None


class DeleteJob(BaseModel):
    id: int | None = None


class DeletedJob(BaseModel):
    id: int | None = None
