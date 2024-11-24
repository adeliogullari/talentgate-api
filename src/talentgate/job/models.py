from enum import Enum
from typing import List

from sqlmodel import SQLModel, Field, Relationship

from src.talentgate.employee.models import Employee


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


class JobSalary(SQLModel, table=True):
    __tablename__ = "job_salary"

    id: int = Field(primary_key=True)
    min: str | None = Field(default=None)
    max: str | None = Field(default=None)
    frequency: str | None = Field(default=None)


class Job(SQLModel, table=True):
    __tablename__ = "job"

    id: int = Field(primary_key=True)
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    workplace: str | None = Field(default=None)
    employment_type: EmploymentType | None = Field(default=None)
    location: JobLocation | None = Relationship(
        back_populates="job", sa_relationship_kwargs={"uselist": False}
    )
    salary: JobSalary | None = Relationship(
        back_populates="job", sa_relationship_kwargs={"uselist": False}
    )
    observer: List["Employee"] = Relationship(back_populates="job")
