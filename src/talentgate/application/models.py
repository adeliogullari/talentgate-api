from enum import Enum
from datetime import datetime, UTC

from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

class ApplicationStatus(str, Enum):
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
    application: Optional["Application"] = Relationship(back_populates="application_link")

class ApplicationEvaluation(SQLModel, table=True):
    __tablename__ = "application_evaluation"

    id: int = Field(primary_key=True)
    text: str | None = Field(default=None)
    application_id: int | None = Field(default=None, foreign_key="application.id")
    application: Optional["Application"] = Relationship(back_populates="evaluations")

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
    )


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
    country: str = Field(default=None)
    postal_code: str | None = Field(default=None)
    resume: str | None = Field(default=None)
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED)
    links: List[ApplicationLink] = Relationship(back_populates="application")
    evaluations: List[ApplicationEvaluation] = Relationship(back_populates="application")

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
    )
