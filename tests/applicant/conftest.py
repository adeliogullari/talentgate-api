from datetime import datetime
import pytest
from config import get_settings
from sqlmodel import Session
from src.talentgate.applicant.models import Applicant

settings = get_settings()


@pytest.fixture
def make_applicant(sqlmodel_session: Session):
    def make(
        firstname: str = "firstname",
        lastname: str = "lastname",
        email: str = "applicant_email@gmail.com",
        phone: str = "+905123456789",
        address: str = "address",
        city: str = "city",
        state: str = "state",
        country: str = "country",
        postal_code: str = "ABC 12345",
        linkedin_url: str = "www.linkedin.com/in/applicant",
        cv_url: str = "cv/applicant.pdf",
        earliest_start_date: datetime = datetime.now(),
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ):
        applicant = Applicant(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            linkedin_url=linkedin_url,
            cv_url=cv_url,
            earliest_start_date=earliest_start_date,
            created_at=created_at,
            updated_at=updated_at,
        )

        sqlmodel_session.add(applicant)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(applicant)

        return applicant

    return make


@pytest.fixture
def applicant(make_applicant):
    return make_applicant()
