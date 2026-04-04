import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.application.enums import ApplicationStatus
from src.talentgate.database.models import BaseModel

if TYPE_CHECKING:
    from src.talentgate.job.models import Job


class ApplicantAddress(SQLModel, table=True):
    __tablename__ = "applicant_address"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    applicant_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    applicant: Optional["Applicant"] = Relationship(back_populates="address")


class ApplicantLink(SQLModel, table=True):
    __tablename__ = "applicant_link"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)
    applicant_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    applicant: Optional["Applicant"] = Relationship(back_populates="links")


class ApplicantEducation(SQLModel, table=True):
    __tablename__ = "applicant_education"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    institution: str | None = Field(default=None)
    degree: str | None = Field(default=None)
    field_of_study: str | None = Field(default=None)
    start_date: str | None = Field(default=None)
    end_date: str | None = Field(default=None)
    applicant_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    applicant: Optional["Applicant"] = Relationship(back_populates="education")


class ApplicantExperience(SQLModel, table=True):
    __tablename__ = "applicant_experience"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str | None = Field(default=None)
    company: str | None = Field(default=None)
    description: str | None = Field(default=None)
    start_date: str | None = Field(default=None)
    end_date: str | None = Field(default=None)
    applicant_id: uuid.UUID | None = Field(default=None, foreign_key="applicant.id", ondelete="CASCADE")
    applicant: Optional["Applicant"] = Relationship(back_populates="experiences")


class Applicant(SQLModel, table=True):
    __tablename__ = "applicant"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    address: ApplicantAddress | None = Relationship(back_populates="applicant", cascade_delete=True)
    links: list[ApplicantLink] | None = Relationship(back_populates="applicant", cascade_delete=True)
    education: ApplicantEducation | None = Relationship(back_populates="applicant", cascade_delete=True)
    experiences: list[ApplicantExperience] | None = Relationship(back_populates="applicant", cascade_delete=True)
    application_id: uuid.UUID | None = Field(default=None, foreign_key="application.id", ondelete="CASCADE")
    application: Optional["Application"] = Relationship(back_populates="applicant")
    created_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class EducationEvaluation(SQLModel, table=True):
    __tablename__ = "education_evaluation"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    score: float | None = Field(default=None)
    evaluation_id: uuid.UUID | None = Field(default=None, foreign_key="evaluation.id", ondelete="CASCADE")
    evaluation: Optional["Evaluation"] = Relationship(back_populates="education_evaluation")


class ExperienceEvaluation(SQLModel, table=True):
    __tablename__ = "experience_evaluation"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    score: float | None = Field(default=None)
    evaluation_id: uuid.UUID | None = Field(default=None, foreign_key="evaluation.id", ondelete="CASCADE")
    evaluation: Optional["Evaluation"] = Relationship(back_populates="experience_evaluation")


class Evaluation(SQLModel, table=True):
    __tablename__ = "evaluation"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    education: EducationEvaluation | None = Relationship(back_populates="evaluation", cascade_delete=True)
    experience: ExperienceEvaluation | None = Relationship(back_populates="evaluation", cascade_delete=True)
    overview: str | None = Field(default=None)
    overall_score: float | None = Field(default=None)
    application_id: uuid.UUID | None = Field(default=None, foreign_key="application.id", ondelete="CASCADE")
    application: Optional["Application"] = Relationship(back_populates="evaluation")


class Application(SQLModel, table=True):
    __tablename__ = "application"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str | None = Field(default=ApplicationStatus.APPLIED.value)
    applicant: Applicant | None = Relationship(back_populates="application", cascade_delete=True)
    evaluation: Evaluation | None = Relationship(back_populates="evaluation", cascade_delete=True)
    job_id: uuid.UUID | None = Field(default=None, foreign_key="job.id", ondelete="CASCADE")
    job: Optional["Job"] = Relationship(back_populates="applications")
    created_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class CreateApplicantAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreatedApplicantAddress(BaseModel):
    id: uuid.UUID | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class RetrievedApplicantAddress(BaseModel):
    id: uuid.UUID | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateApplicantLink(BaseModel):
    type: str | None = None
    url: str | None = None


class CreatedApplicantLink(BaseModel):
    id: uuid.UUID | None = None
    type: str | None = None
    url: str | None = None


class RetrievedApplicantLink(BaseModel):
    id: uuid.UUID | None = None
    type: str | None = None
    url: str | None = None


class UpdateApplicantLink(BaseModel):
    type: str | None = None
    url: str | None = None


class UpdatedApplicantLink(BaseModel):
    id: uuid.UUID | None = None
    type: str | None = None
    url: str | None = None


class CreateApplicantEducation(BaseModel):
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class CreatedApplicantEducation(BaseModel):
    id: uuid.UUID | None = None
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class RetrievedApplicantEducation(BaseModel):
    id: uuid.UUID | None = None
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class UpdateApplicantEducation(BaseModel):
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class UpdatedApplicantEducation(BaseModel):
    id: uuid.UUID | None = None
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class CreateApplicantExperience(BaseModel):
    title: str | None = None
    company: str | None = None
    description: str | None = None
    skills: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class CreatedApplicantExperience(BaseModel):
    id: uuid.UUID | None = None
    title: str | None = None
    company: str | None = None
    description: str | None = None
    skills: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class RetrievedApplicantExperience(BaseModel):
    id: uuid.UUID | None = None
    title: str | None
    company: str | None
    description: str | None
    skills: str | None
    start_date: str | None
    end_date: str | None


class UpdateApplicantExperience(BaseModel):
    title: str | None = None
    company: str | None = None
    description: str | None = None
    skills: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class UpdatedApplicantExperience(BaseModel):
    id: uuid.UUID | None = None
    title: str | None = None
    company: str | None = None
    description: str | None = None
    skills: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class CreateApplicant(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    address: CreateApplicantAddress | None = None
    links: list[CreateApplicantLink] | None = None
    education: ApplicantEducation | None = None
    experiences: list[ApplicantExperience] | None = None


class CreatedApplicant(BaseModel):
    id: uuid.UUID | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    address: CreatedApplicantAddress | None = None
    links: list[CreatedApplicantLink] | None = None
    education: CreatedApplicantEducation | None = None
    experiences: list[CreatedApplicantExperience] | None = None
    created_at: float
    updated_at: float


class RetrievedApplicant(BaseModel):
    id: uuid.UUID | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    address: RetrievedApplicantAddress | None = None
    links: list[RetrievedApplicantLink] | None = None
    education: RetrievedApplicantEducation | None = None
    experiences: list[RetrievedApplicantExperience] | None = None
    created_at: float
    updated_at: float


class CreateEducationEvaluation(BaseModel):
    score: float | None = None


class CreatedEducationEvaluation(BaseModel):
    id: uuid.UUID | None = None
    score: float | None = None


class RetrievedEducationEvaluation(BaseModel):
    id: uuid.UUID | None = None
    score: float | None = None


class CreateExperienceEvaluation(BaseModel):
    score: float | None = None


class CreatedExperienceEvaluation(BaseModel):
    id: uuid.UUID | None = None
    score: float | None = None


class RetrievedExperienceEvaluation(BaseModel):
    id: uuid.UUID | None = None
    score: float | None = None


class CreateEvaluation(BaseModel):
    education: CreatedEducationEvaluation | None = None
    experience: CreatedExperienceEvaluation | None = None
    overview: str | None = Field(default=None)
    overall_score: float | None = Field(default=None)


class CreatedEvaluation(BaseModel):
    education: EducationEvaluation | None = Relationship(back_populates="evaluation", cascade_delete=True)
    experience: ExperienceEvaluation | None = Relationship(back_populates="evaluation", cascade_delete=True)
    overview: str | None = Field(default=None)
    overall_score: float | None = Field(default=None)


class RetrievedEvaluation(BaseModel):
    education: EducationEvaluation | None = Relationship(back_populates="evaluation", cascade_delete=True)
    experience: ExperienceEvaluation | None = Relationship(back_populates="evaluation", cascade_delete=True)
    overview: str | None = Field(default=None)
    overall_score: float | None = Field(default=None)


class CreateApplication(BaseModel):
    applicant: CreateApplicant | None = None
    evaluation: CreateEvaluation | None = None
    status: str | None = None


class CreatedApplication(BaseModel):
    id: uuid.UUID | None = None
    applicant: CreatedApplicant | None = None
    evaluation: CreatedEvaluation | None = None
    status: str | None = None
    created_at: float
    updated_at: float


class RetrievedApplication(BaseModel):
    id: uuid.UUID | None = None
    applicant: RetrievedApplicant | None = None
    evaluation: RetrievedEvaluation | None = None
    status: str | None = None
    created_at: float
    updated_at: float


class ApplicationQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None


class DeletedApplication(BaseModel):
    id: uuid.UUID | None = None
