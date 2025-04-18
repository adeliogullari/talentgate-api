from typing import BinaryIO

import pytest
from minio import Minio

from config import get_settings
from sqlmodel import Session
from src.talentgate.application.models import Application, ApplicationEvaluation
from src.talentgate.employee.models import Employee

settings = get_settings()


@pytest.fixture
def make_application_evaluation(
    sqlmodel_session: Session, employee: Employee, application: Application
):
    def make(
        comment: str = "text123",
        rating: str = "5",
        employee_id: int = employee.id,
        application_id: int = application.id,
    ):
        evaluation = ApplicationEvaluation(
            comment=comment,
            rating=rating,
            employee_id=employee_id,
            application_id=application_id,
        )

        sqlmodel_session.add(evaluation)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(evaluation)

        return evaluation

    return make


@pytest.fixture
def application_evaluation(make_application_evaluation):
    return make_application_evaluation()


@pytest.fixture
def make_resume(minio_client: Minio):
    def make(
        bucket_name: str = "resume",
        object_name: str = "resume",
        data: BinaryIO = b"resume",
        length: int = 0,
    ):
        return minio_client.put_object(
            bucket_name=bucket_name, object_name=object_name, data=data, length=length
        )

    return make


@pytest.fixture
def resume(make_resume):
    return make_resume()


@pytest.fixture
def make_application(sqlmodel_session: Session):
    def make(
        firstname: str = "firstname",
        lastname: str = "lastname",
        email: str = "applicant_email@gmail.com",
        phone: str = "+905123456789",
        resume: str = "resume",
        employee_id: int = None,
        application_id: int = None,
    ):
        application = Application(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            resume=resume,
            employee_id=employee_id,
            application_id=application_id,
        )

        sqlmodel_session.add(application)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(application)

        return application

    return make


@pytest.fixture
def application(make_application):
    return make_application()
