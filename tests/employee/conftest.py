import pytest
from sqlmodel import Session
from src.talentgate.employee.models import Employee, EmployeeTitle


@pytest.fixture
def make_employee(sqlmodel_session: Session):
    def make(
        title=EmployeeTitle.RECRUITER,
    ):
        employee = Employee(title=title)

        sqlmodel_session.add(employee)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(employee)

        return employee

    return make


@pytest.fixture
def employee(make_employee):
    return make_employee()
