from enum import StrEnum
from datetime import datetime, UTC
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


class CompanyLocationType(StrEnum):
    HEADQUARTERS = "Headquarters"
    OFFICE = "Office"


class CompanyLocation(SQLModel, table=True):
    __tablename__ = "company_location"

    id: int = Field(primary_key=True)
    type: CompanyLocationType | None = Field(default=CompanyLocationType.OFFICE)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    address_id: int | None = Field(default=None, foreign_key="company_address.id")
    address: Optional[CompanyAddress] = Relationship(back_populates="location")
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(back_populates="locations")


class LinkType(StrEnum):
    WEBSITE = "Website"
    LINKEDIN = "LinkedIn"
    GITHUB = "Github"


class CompanyLink(SQLModel, table=True):
    __tablename__ = "company_link"

    id: int = Field(primary_key=True)
    type: LinkType | None = Field(default=LinkType.WEBSITE)
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
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp()
    )
    updated_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )

    @property
    def subscription(self):
        return next(
            filter(lambda employee: employee.title == "Founder", self.employees), None
        ).user.subscription


class CompanyEmployee(BaseModel):
    id: int | None = None
    title: str | None = None


class CreateAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreatedAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class RetrievedAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdateAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdatedAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateLocation(BaseModel):
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateAddress | None = None


class CreatedLocation(BaseModel):
    id: int
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateAddress | None = None


class RetrievedLocation(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdateLocation(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdatedLocation(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateLink(SQLModel):
    type: str | None = None
    url: str | None = None


class CreatedLink(SQLModel):
    id: int
    type: str | None = None
    url: str | None = None


class RetrievedLink(BaseModel):
    id: int
    type: str | None = None
    url: str | None = None


class UpdateLink(BaseModel):
    type: str | None = None
    url: str | None = None


class UpdatedLink(BaseModel):
    id: int
    type: str | None = None
    url: str | None = None


class CreateCompany(BaseModel):
    name: str
    overview: str | None = None
    locations: List[CreateLocation] | None = None
    links: List[CreateLink] | None = None
    jobs: List | None = None


class CreatedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: List[CompanyEmployee] | None = None
    locations: List[CompanyLocation] | None = None
    links: List[CreatedLink] | None = None
    created_at: float
    updated_at: float


class RetrievedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: List[CompanyEmployee] | None = None
    locations: List[CompanyLocation] | None = None
    created_at: float
    updated_at: float


class CompanyQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    name: str | None = None


class UpdateCompany(BaseModel):
    name: str
    overview: str | None = None
    locations: List[CompanyLocation] | None = None
    links: List[CompanyLink] | None = None
    employees: List[CompanyEmployee] | None = None
    jobs: List | None = None


class UpdatedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: List[CompanyEmployee] | None = None
    locations: List[CompanyLocation] | None = None
    links: List[CompanyLink] | None = None
    created_at: float
    updated_at: float


class DeletedCompany(SQLModel):
    id: int
