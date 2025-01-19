from enum import StrEnum
from datetime import datetime, UTC

from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.employee.models import Employee
from src.talentgate.job.models import Job


class ApplicationStatus(StrEnum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    REFERENCE_CHECK = "Reference Check"
    OFFER = "Offer"
    WITHDRAWN = "Withdrawn"


class ApplicationLink(SQLModel, table=True):
    __tablename__ = "application_link"

    id: int = Field(primary_key=True)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)
    application_id: int | None = Field(default=None, foreign_key="application.id")
    application: Optional["Application"] = Relationship(back_populates="links")


class ApplicationEvaluation(SQLModel, table=True):
    __tablename__ = "application_evaluation"

    id: int = Field(primary_key=True)
    comment: str | None = Field(nullable=False)
    rating: int | None = Field(default=None, ge=0, le=5)
    employee_id: int | None = Field(default=None, foreign_key="employee.id")
    employee: Optional["Employee"] = Relationship(
        back_populates="application_evaluations"
    )
    application_id: int | None = Field(default=None, foreign_key="application.id")
    application: Optional["Application"] = Relationship(back_populates="evaluations")

    created_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
    )


class ApplicationEvaluationRequest(SQLModel):
    comment: str | None = None
    rating: int | None = None
    employee_id: int | None = None
    application_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ApplicationEvaluationQueryParameters(SQLModel):
    offset: int | None = None
    limit: int | None = None


class ApplicationEvaluationResponse(SQLModel):
    id: int | None = None
    comment: str | None = None
    rating: int | None = None
    employee_id: int | None = None
    application_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Application(SQLModel, table=True):
    __tablename__ = "application"

    id: int = Field(primary_key=True)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    email: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    resume: str = Field(default=None)
    earliest_start_date: Optional[datetime] = None
    links: List[ApplicationLink] = Relationship(back_populates="application")
    status: ApplicationStatus | None = Field(default=ApplicationStatus.APPLIED)
    evaluations: List[ApplicationEvaluation] = Relationship(
        back_populates="application"
    )
    job_id: int | None = Field(default=None, foreign_key="job.id")
    job: Optional["Job"] = Relationship(back_populates="applications")

    created_at: datetime | None = Field(default=datetime.now(UTC))
    updated_at: datetime | None = Field(
        default=datetime.now(UTC),
        sa_column_kwargs={"onupdate": datetime.now(UTC)},
    )


class ApplicationRequest(SQLModel):
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
    earliest_start_date: datetime | None = None
    status: ApplicationStatus | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ApplicationResponse(SQLModel):
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
    earliest_start_date: datetime | None = None
    status: ApplicationStatus | None = None
    links: List[ApplicationLink] = None
    evaluations: List[ApplicationEvaluation] = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateApplication(ApplicationRequest):
    pass


class CreatedApplication(ApplicationResponse):
    pass


class RetrievedApplication(ApplicationResponse):
    pass


class ApplicationQueryParameters(SQLModel):
    offset: int | None = None
    limit: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None


class UpdateApplication(ApplicationRequest):
    pass


class UpdatedApplication(ApplicationResponse):
    pass


class DeleteApplication(SQLModel):
    id: int


class DeletedApplication(SQLModel):
    id: int
