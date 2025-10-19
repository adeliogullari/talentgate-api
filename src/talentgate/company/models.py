from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.company.enums import CompanyLocationType, LinkType
from src.talentgate.database.models import BaseModel
from src.talentgate.user.models import UserSubscription

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
    type: str | None = Field(default=CompanyLocationType.OFFICE.value)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    address_id: int | None = Field(default=None, foreign_key="company_address.id")
    address: CompanyAddress | None = Relationship(
        back_populates="location",
        sa_relationship_kwargs={"uselist": False},
    )
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(back_populates="locations")


class CompanyLink(SQLModel, table=True):
    __tablename__ = "company_link"

    id: int = Field(primary_key=True)
    type: str | None = Field(default=LinkType.WEBSITE.value)
    url: str | None = Field(default=None, max_length=2048)
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(
        back_populates="links",
        sa_relationship_kwargs={"cascade": "all"},
    )


class Company(SQLModel, table=True):
    __tablename__ = "company"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    overview: str | None = Field(default=None)
    logo: str | None = Field(default=None)
    employees: list["Employee"] = Relationship(
        back_populates="company",
        sa_relationship_kwargs={"cascade": "all"},
    )
    locations: list[CompanyLocation] = Relationship(
        back_populates="company",
        sa_relationship_kwargs={"cascade": "all"},
    )
    links: list[CompanyLink] = Relationship(
        back_populates="company",
        sa_relationship_kwargs={"cascade": "all"},
    )
    jobs: list["Job"] = Relationship(
        back_populates="company",
        sa_relationship_kwargs={"cascade": "all"},
    )
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )

    @property
    def subscription(self) -> UserSubscription:
        return next(
            filter(lambda employee: employee.title == "Founder", self.employees),
            None,
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
    locations: list[CreateLocation] | None = None
    links: list[CreateLink] | None = None
    jobs: list | None = None


class CreatedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: list[CompanyEmployee] | None = None
    locations: list[CompanyLocation] | None = None
    links: list[CreatedLink] | None = None
    created_at: float
    updated_at: float


class RetrievedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: list[CompanyEmployee] | None = None
    locations: list[CompanyLocation] | None = None
    links: list[RetrievedLink] | None = None
    created_at: float
    updated_at: float


class RetrievedCurrentCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: list[CompanyEmployee] | None = None
    locations: list[CompanyLocation] | None = None
    links: list[RetrievedLink] | None = None
    created_at: float
    updated_at: float


class CompanyQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    name: str | None = None


class UpdateCompany(BaseModel):
    name: str
    overview: str | None = None
    locations: list[CompanyLocation] | None = None
    links: list[CompanyLink] | None = None
    employees: list[CompanyEmployee] | None = None
    jobs: list | None = None


class UpdatedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: list[CompanyEmployee] | None = None
    locations: list[CompanyLocation] | None = None
    links: list[CompanyLink] | None = None
    created_at: float
    updated_at: float


class DeletedCompany(SQLModel):
    id: int
