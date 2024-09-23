from sqlmodel import SQLModel, Field


class ApplicationOffer(SQLModel, table=True):
    __tablename__ = "application_offer"

    id: int = Field(primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)


class Application(SQLModel, table=True):
    __tablename__ = "application"

    id: int = Field(primary_key=True)
    status: bool | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
