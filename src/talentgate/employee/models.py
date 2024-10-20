from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.user.models import User


class EmployeeRole(str, Enum):
    FOUNDER = "founder"
    HR_MANAGER = "hr_manager"
    RECRUITER = "recruiter"


class EmployeeSalary(SQLModel, table=True):
    __tablename__ = "employee_salary"

    id: int = Field(primary_key=True)
    amount: float | None = Field(default=None)
    currency: str | None = Field(default=None)


class Employee(SQLModel, table=True):
    __tablename__ = "employee"

    id: int = Field(primary_key=True)
    title: str | None = Field(default=None)
    user: User = Relationship(back_populates="employee")
    salary: EmployeeSalary | None = Relationship(back_populates="employee")
    role: EmployeeRole | None = Field(default=None)
