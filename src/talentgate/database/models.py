from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    model_config = {
        "extra": "forbid",
        "from_attributes": True,
    }


class Observer(SQLModel, table=True):
    __tablename__ = "observer"

    employee_id: int = Field(default=None, foreign_key="employee.id", primary_key=True)
    job_id: int = Field(default=None, foreign_key="job.id", primary_key=True)
