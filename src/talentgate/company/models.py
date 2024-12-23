from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


class CompanyLocationAddress(SQLModel, table=True):
    __tablename__ = "company_location_address"

    id: int = Field(primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)


class CompanyLocation(SQLModel, table=True):
    __tablename__ = "company_location"

    id: int = Field(primary_key=True)
    type: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    address: CompanyLocationAddress = Relationship(
        back_populates="company", sa_relationship_kwargs={"uselist": False}
    )
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(back_populates="company_location")


class CompanyLink(SQLModel, table=True):
    __tablename__ = "company_link"

    id: int = Field(primary_key=True)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(back_populates="company_link")


class Company(SQLModel, table=True):
    __tablename__ = "company"

    id: int = Field(primary_key=True)
    name: str | None = Field(default=None)
    overview: str | None = Field(default=None)
    locations: List[CompanyLocation] = Relationship(back_populates="company")
    links: List[CompanyLink] = Relationship(back_populates="company")


class CompanyRequest(SQLModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    password: str
    verified: bool | None = None


class CompanyResponse(SQLModel):
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str
    email: str
    verified: bool | None = None


class CreateCompany(CompanyRequest):
    pass


class CreatedCompany(CompanyResponse):
    pass


class RetrievedCompany(CompanyResponse):
    pass


class CompanyQueryParameters(SQLModel):
    offset: int | None = None
    limit: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None
    verified: bool | None = None


class UpdateCompany(CompanyRequest):
    pass


class UpdatedCompany(CompanyResponse):
    pass


class DeletedCompany(SQLModel):
    id: int
