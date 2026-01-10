from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.application.enums import ApplicationStatus

if TYPE_CHECKING:
    from src.talentgate.job.models import Job


class ApplicationAddress(SQLModel, table=True):
    __tablename__ = "application_address"

    id: int = Field(primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    application_id: int | None = Field(default=None, foreign_key="application.id", ondelete="CASCADE")
    application: Optional["Application"] = Relationship(back_populates="address")


class ApplicationLink(SQLModel, table=True):
    __tablename__ = "application_link"

    id: int = Field(primary_key=True)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)
    application_id: int | None = Field(default=None, foreign_key="application.id", ondelete="CASCADE")
    application: Optional["Application"] = Relationship(back_populates="links")


class Application(SQLModel, table=True):
    __tablename__ = "application"

    id: int = Field(primary_key=True)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    email: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    resume: str | None = Field(default=None)
    status: str | None = Field(default=ApplicationStatus.APPLIED.value)
    address: ApplicationAddress | None = Relationship(back_populates="application", cascade_delete=True)
    links: list[ApplicationLink] = Relationship(back_populates="application", cascade_delete=True)
    job_id: int | None = Field(default=None, foreign_key="job.id")
    job: Optional["Job"] = Relationship(back_populates="applications")
    created_at: datetime | None = Field(default=datetime.now(UTC))
    updated_at: datetime | None = Field(
        default=datetime.now(UTC),
        sa_column_kwargs={"onupdate": datetime.now(UTC)},
    )


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
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    resume: str | None = None
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
    resume: str | None = None
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
    resume: str | None = None
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
    resume: Any | None = None
    earliest_start_date: datetime | None = None
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
    resume: Any | None = None
    earliest_start_date: datetime | None = None
    status: str | None = None
    links: list[ApplicationLink] = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DeleteApplication(SQLModel):
    id: int


class DeletedApplication(SQLModel):
    id: int
