from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.talentgate.employee.models import Employee
    from src.talentgate.job.models import Job


class Observer(SQLModel, table=True):
    __tablename__ = "observer"

    id: int = Field(primary_key=True)
    employee_id: int = Field(
        default=None, foreign_key="employee.id", nullable=False, ondelete="CASCADE"
    )
    employee: Optional["Employee"] = Relationship(back_populates="observed_jobs")
    job_id: int = Field(
        default=None, foreign_key="job.id", nullable=False, ondelete="CASCADE"
    )
    job: Optional["Job"] = Relationship(back_populates="observers")
    created_at: datetime | None = Field(default=datetime.now(UTC))
    updated_at: datetime | None = Field(
        default=datetime.now(UTC),
        sa_column_kwargs={"onupdate": datetime.now(UTC)},
    )


class ObserverRequest(SQLModel):
    job_id: int | None = None
    employee_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ObserverResponse(SQLModel):
    id: int | None = None
    job_id: int | None = None
    employee_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ObserverQueryParameters(SQLModel):
    offset: int | None = None
    limit: int | None = None


class CreateObserver(ObserverRequest):
    pass


class CreatedObserver(ObserverResponse):
    pass


class RetrievedObserver(ObserverResponse):
    pass


class UpdateObserver(ObserverRequest):
    pass


class UpdatedObserver(ObserverResponse):
    pass


class DeleteObserver(ObserverRequest):
    pass


class DeletedObserver(ObserverResponse):
    pass
