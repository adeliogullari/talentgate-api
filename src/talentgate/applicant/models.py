from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from typing import Optional

class BaseApplicant(SQLModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: str
    phone: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    linkedin_url: Optional[str] = None
    cv_url: Optional[str] = None
    earliest_start_date: Optional[datetime] = None

class Applicant(BaseApplicant, table=True):
    __tablename__ = "applicant"
    
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)}
    )

class ApplicantRequest(BaseApplicant):
    pass

class ApplicantResponse(BaseApplicant):
    id: int
    created_at: datetime
    updated_at: datetime

class ApplicantQueryParameters(SQLModel):
    offset: Optional[int] = None
    limit: Optional[int] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class CreateApplicant(ApplicantRequest):
    pass

class CreatedApplicant(ApplicantResponse):
    pass

class UpdateApplicant(ApplicantRequest):
    pass

class UpdatedApplicant(ApplicantResponse):
    pass

class DeleteApplicant(SQLModel):
    id: int

class DeletedApplicant(SQLModel):
    id: int