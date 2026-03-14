import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.application.enums import ApplicationStatus

if TYPE_CHECKING:
    from src.talentgate.job.models import Job


class ApplicantAddress(SQLModel, table=True):
    __tablename__ = "applicant_address"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    applicant_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    applicant: Optional["Applicant"] = Relationship(back_populates="address")


class ApplicantLink(SQLModel, table=True):
    __tablename__ = "applicant_link"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)
    applicant_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    applicant: Optional["Applicant"] = Relationship(back_populates="links")


class ApplicantEducation(SQLModel, table=True):
    __tablename__ = "applicant_education"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    institution: str | None = Field(default=None)
    degree: str | None = Field(default=None)
    field_of_study: str | None = Field(default=None)
    start_date: str | None = Field(default=None)
    end_date: str | None = Field(default=None)
    applicant_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    applicant: Optional["Applicant"] = Relationship(back_populates="education")


class ApplicantExperience(SQLModel, table=True):
    __tablename__ = "applicant_experience"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str | None = Field(default=None)
    company: str | None = Field(default=None)
    description: str | None = Field(default=None)
    skills: str | None = Field(default=None)
    start_date: str | None = Field(default=None)
    end_date: str | None = Field(default=None)
    applicant_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    applicant: Optional["Applicant"] = Relationship(back_populates="experiences")


class Applicant(SQLModel, table=True):
    __tablename__ = "applicant"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    address: ApplicantAddress | None = Relationship(back_populates="applicant", cascade_delete=True)
    links: list[ApplicantLink] | None = Relationship(back_populates="applicant", cascade_delete=True)
    education: ApplicantEducation | None = Relationship(back_populates="applicant", cascade_delete=True)
    experiences: list[ApplicantExperience] | None = Relationship(back_populates="applicant", cascade_delete=True)
    application_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    application: Optional["Application"] = Relationship(back_populates="applicant")
    created_at: datetime | None = Field(default=datetime.now(UTC))
    updated_at: datetime | None = Field(
        default=datetime.now(UTC),
        sa_column_kwargs={"onupdate": datetime.now(UTC)},
    )


class Application(SQLModel, table=True):
    __tablename__ = "application"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str | None = Field(default=ApplicationStatus.APPLIED.value)
    applicant: Applicant | None = Relationship(back_populates="application", cascade_delete=True)
    job_id: uuid.UUID | None = Field(default=None, foreign_key="job.id", ondelete="CASCADE")
    job: Optional["Job"] = Relationship(back_populates="applications")
    created_at: datetime | None = Field(default=datetime.now(UTC))
    updated_at: datetime | None = Field(
        default=datetime.now(UTC),
        sa_column_kwargs={"onupdate": datetime.now(UTC)},
    )


class CreateApplicantAddress(SQLModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreatedApplicantAddress(SQLModel):
    id: uuid.UUID
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class RetrievedApplicantAddress(SQLModel):
    id: uuid.UUID
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateApplicationAddress(SQLModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreatedApplicationAddress(SQLModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class RetrievedApplicationAddress(SQLModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdateApplicationAddress(SQLModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdatedApplicationAddress(SQLModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateApplicationLink(SQLModel):
    type: str | None = None
    url: str | None = None


class CreatedApplicationLink(SQLModel):
    id: int
    type: str | None = None
    url: str | None = None


class RetrievedApplicationLink(SQLModel):
    id: int
    type: str | None = None
    url: str | None = None


class UpdateApplicationLink(SQLModel):
    type: str | None = None
    url: str | None = None


class UpdatedApplicationLink(SQLModel):
    id: int
    type: str | None = None
    url: str | None = None


class CreateApplication(SQLModel):
    firstname: str
    lastname: str
    email: str
    phone: str
    address: CreateApplicationAddress | None = None
    links: list[CreateApplicationLink] | None = None
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreatedApplication(SQLModel):
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    status: str | None = None
    links: list[ApplicationLink] = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RetrievedApplication(SQLModel):
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    status: str | None = None
    links: list[ApplicationLink] = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ApplicationQueryParameters(SQLModel):
    offset: int | None = None
    limit: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None


class UpdateApplication(SQLModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UpdatedApplication(SQLModel):
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    status: str | None = None
    links: list[ApplicationLink] = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DeleteApplication(SQLModel):
    id: int


class DeletedApplication(SQLModel):
    id: int
