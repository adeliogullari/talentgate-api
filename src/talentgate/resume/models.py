from datetime import date

from pydantic import Field

from src.talentgate.database.models import BaseModel


class Experience(BaseModel):
    company: str | None = None
    title: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None


class Education(BaseModel):
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class ParsedResume(BaseModel):
    summary: str | None = None
    experiences: list[Experience] = Field(default_factory=list)
    educations: list[Education] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
