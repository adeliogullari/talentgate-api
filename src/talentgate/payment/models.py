from src.talentgate.database.models import BaseModel


class CreateCompany(BaseModel):
    name: str
    overview: str | None = None
    jobs: list | None = None


class PaddleCheckout(BaseModel):
    name: str
    overview: str | None = None
    jobs: list | None = None
