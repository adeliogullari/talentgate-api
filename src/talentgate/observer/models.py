from datetime import datetime

from sqlmodel import SQLModel, Field


class Observer(SQLModel, table=True):
    __tablename__ = "observer"

    employee_id: int | None = Field(default=None, foreign_key="employee.id", primary_key=True)
    job_id: int | None = Field(default=None, foreign_key="job.id", primary_key=True)
