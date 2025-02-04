from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.talentgate.database.models import BaseModel

if TYPE_CHECKING:
    from src.talentgate.employee.models import Employee
    from src.talentgate.job.models import Job


class CompanyAddress(SQLModel, table=True):
    __tablename__ = "company_address"

    id: int = Field(primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    location: Optional["CompanyLocation"] = Relationship(
        back_populates="address",
        sa_relationship_kwargs={"uselist": False},
    )


class CompanyLocation(SQLModel, table=True):
    __tablename__ = "company_location"

    id: int = Field(primary_key=True)
    type: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    address_id: int | None = Field(default=None, foreign_key="company_address.id")
    address: Optional[CompanyAddress] = Relationship(back_populates="location")

    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(back_populates="locations")


class CompanyLink(SQLModel, table=True):
    __tablename__ = "company_link"

    id: int = Field(primary_key=True)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(
        back_populates="links", sa_relationship_kwargs={"cascade": "all"}
    )


class Company(SQLModel, table=True):
    __tablename__ = "company"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    overview: str | None = Field(default=None)
    employees: List["Employee"] = Relationship(
        back_populates="company", sa_relationship_kwargs={"cascade": "all"}
    )
    locations: List[CompanyLocation] = Relationship(
        back_populates="company", sa_relationship_kwargs={"cascade": "all"}
    )
    links: List[CompanyLink] = Relationship(
        back_populates="company", sa_relationship_kwargs={"cascade": "all"}
    )
    jobs: List["Job"] = Relationship(
        back_populates="company", sa_relationship_kwargs={"cascade": "all"}
    )


class CompanyEmployee(BaseModel):
    id: int | None = None
    title: str | None = None


class CreateAddress(SQLModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreatedAddress(SQLModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateLocation(SQLModel):
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateAddress | None = None


class CreatedLocation(SQLModel):
    id: int
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateAddress | None = None


class CreateLink(SQLModel):
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)


class CreatedLink(SQLModel):
    id: int
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)


class CreateCompany(BaseModel):
    name: str
    overview: str | None = None
    locations: List[CompanyLocation] | None = None
    jobs: List | None = None


class CreatedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: List[CompanyEmployee] | None = None
    locations: List[CompanyLocation] | None = None


class RetrievedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: List[CompanyEmployee] | None = None
    locations: List[CompanyLocation] | None = None


class CompanyQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    name: str | None = None


class UpdateCompany(BaseModel):
    name: str
    overview: str | None = None
    locations: List[CompanyLocation] | None = None
    jobs: List | None = None


class UpdatedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: List[CompanyEmployee] | None = None
    locations: List[CompanyLocation] | None = None


class DeletedCompany(SQLModel):
    id: int
