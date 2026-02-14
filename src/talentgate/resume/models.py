from src.talentgate.database.models import BaseModel


class ResumeParse(BaseModel):
    id: int | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None

class EducationEvaluation(BaseModel):
    score: float | None = None


class ResumeEvaluation(BaseModel):
    score: float | None = None
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
