import pytest
from sqlmodel import Session

from src.talentgate.employee.enums import EmployeeTitle
from src.talentgate.employee.models import Employee
from src.talentgate.user.models import User


@pytest.fixture
def make_employee(sqlmodel_session: Session, user: User):
    def make(**kwargs):
        employee = Employee(
            title=kwargs.get("title") or EmployeeTitle.RECRUITER,
            user=kwargs.get("user") or user,
        )

        sqlmodel_session.add(employee)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(employee)

        return employee

    return make


@pytest.fixture
def employee(make_employee, request):
    param = getattr(request, "param", {})
    title = param.get("title", None)

    return make_employee(
        title=title,
    )
