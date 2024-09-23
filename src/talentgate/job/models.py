from sqlmodel import SQLModel, Field, Relationship


class JobLocation(SQLModel, table=True):
    __tablename__ = "job_location"

    id: int = Field(primary_key=True)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)


class JobSalaryCurrency(SQLModel, table=True):
    __tablename__ = "job_salary_currency"

    name: str | None = Field(default=None)
    symbol: str | None = Field(default=None)


class JobSalary(SQLModel, table=True):
    __tablename__ = "job_salary"

    id: int = Field(primary_key=True)
    min: str | None = Field(default=None)
    max: str | None = Field(default=None)
    currency: JobSalaryCurrency = Relationship(back_populates="job_salary")


class Job(SQLModel, table=True):
    __tablename__ = "job"

    id: int = Field(primary_key=True)
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    workplace: str | None = Field(default=None)
    employment: str | None = Field(default=None)
    location: JobLocation = Relationship(
        back_populates="job", sa_relationship_kwargs={"uselist": False}
    )
    salary: JobSalary = Relationship(
        back_populates="job", sa_relationship_kwargs={"uselist": False}
    )
