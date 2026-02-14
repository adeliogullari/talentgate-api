from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.talentgate.company.enums import CompanyEmployeeTitle
from src.talentgate.database.models import BaseModel
from src.talentgate.user.models import (
    CreatedUser,
    CreateUser,
    RetrievedUser,
    UpdatedUser,
    UpdateUser,
    User,
    UserQueryParameters,
    UserSubscription,
)

if TYPE_CHECKING:
    from src.talentgate.job.models import Job, RetrievedJobLocation, RetrievedJobSalary


class CompanyLocationAddress(SQLModel, table=True):
    __tablename__ = "company_location_address"

    id: int | None = Field(default=None, primary_key=True)
    unit: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    location_id: int | None = Field(default=None, foreign_key="company_location.id", ondelete="CASCADE")
    location: Optional["CompanyLocation"] = Relationship(back_populates="address")


class CompanyLocation(SQLModel, table=True):
    __tablename__ = "company_location"

    id: int | None = Field(default=None, primary_key=True)
    type: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    address: CompanyLocationAddress | None = Relationship(back_populates="location", cascade_delete=True)
    company_id: int | None = Field(default=None, foreign_key="company.id", ondelete="CASCADE")
    company: Optional["Company"] = Relationship(back_populates="locations")


class CompanyLink(SQLModel, table=True):
    __tablename__ = "company_link"

    id: int | None = Field(default=None, primary_key=True)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)
    company_id: int | None = Field(default=None, foreign_key="company.id", ondelete="CASCADE")
    company: Optional["Company"] = Relationship(
        back_populates="links",
    )


class CompanyInvitation(SQLModel, table=True):
    __tablename__ = "company_invitation"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    status: str | None = Field(default=None)
    company_id: int | None = Field(default=None, foreign_key="company.id", ondelete="CASCADE")
    company: Optional["Company"] = Relationship(back_populates="invitations")
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class CompanyEmployee(SQLModel, table=True):
    __tablename__ = "company_employee"

    id: int = Field(primary_key=True)
    title: str | None = Field(default=None)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="employee")
    company_id: int | None = Field(default=None, foreign_key="company.id", ondelete="CASCADE")
    company: None | "Company" = Relationship(back_populates="employees")
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )


class Company(SQLModel, table=True):
    __tablename__ = "company"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    overview: str | None = Field(default=None)
    logo: str | None = Field(default=None)
    locations: list[CompanyLocation] = Relationship(
        back_populates="company",
        cascade_delete=True,
    )
    links: list[CompanyLink] = Relationship(
        back_populates="company",
        cascade_delete=True,
    )
    invitations: list["CompanyInvitation"] = Relationship(back_populates="company", cascade_delete=True)
    employees: list["CompanyEmployee"] = Relationship(back_populates="company", cascade_delete=True)
    jobs: list["Job"] = Relationship(
        back_populates="company",
        cascade_delete=True,
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
            filter(lambda employee: employee.title == CompanyEmployeeTitle.FOUNDER.value, self.employees),
            None,
        ).user.subscription


class RetrievedCurrentCompanyJob(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    department: str | None = None
    employment_type: str | None = None
    location: Optional["RetrievedJobLocation"] = None
    salary: Optional["RetrievedJobSalary"] = None


class CreateCompanyLocationAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreatedCompanyLocationAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class RetrievedCompanyLocationAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdateCompanyLocationAddress(BaseModel):
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class UpdatedCompanyLocationAddress(BaseModel):
    id: int
    unit: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CreateCompanyLocation(BaseModel):
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreateCompanyLocationAddress | None = None


class CreatedCompanyLocation(BaseModel):
    id: int
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: CreatedCompanyLocationAddress | None = None


class RetrievedCompanyLocation(BaseModel):
    id: int
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: RetrievedCompanyLocationAddress | None = None


class UpdateCompanyLocation(BaseModel):
    id: int | None = None
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: UpdateCompanyLocationAddress | None = None


class UpdatedCompanyLocation(BaseModel):
    id: int
    type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: UpdatedCompanyLocationAddress | None = None


class CreateCompanyLink(SQLModel):
    type: str | None = None
    url: str | None = None


class CreatedCompanyLink(SQLModel):
    id: int
    type: str | None = None
    url: str | None = None


class RetrievedCompanyLink(BaseModel):
    id: int
    type: str | None = None
    url: str | None = None


class UpdateCompanyLink(BaseModel):
    id: int | None = None
    type: str | None = None
    url: str | None = None


class UpdatedCompanyLink(BaseModel):
    id: int
    type: str | None = None
    url: str | None = None


class CreateCompanyInvitation(BaseModel):
    email: str
    status: str | None = None


class RetrievedCompanyInvitation(BaseModel):
    id: int | None = None
    email: str
    status: str | None = None
    start_date: float | None = None
    end_date: float | None = None


class UpdateCompanyInvitation(BaseModel):
    email: str
    status: str | None = None


class UpsertCompanyInvitation(BaseModel):
    email: str
    status: str | None = None


class DeleteCompanyInvitation(BaseModel):
    id: int


class CreateCompanyEmployee(BaseModel):
    title: str | None = None
    user: CreateUser | None = None


class CreatedCompanyEmployee(BaseModel):
    id: int
    title: str | None = None
    user: CreatedUser | None = None
    created_at: float
    updated_at: float


class RetrievedCompanyEmployee(BaseModel):
    id: int
    title: str | None = None
    user: RetrievedUser | None = None
    created_at: float
    updated_at: float


class CompanyEmployeeQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    id: int | None = None
    title: str | None = None
    user: UserQueryParameters | None = None


class UpdateCompanyEmployee(BaseModel):
    title: str | None = None
    user: UpdateUser | None = None


class UpdatedCompanyEmployee(BaseModel):
    id: int
    title: str | None = None
    user: UpdatedUser | None = None
    created_at: float
    updated_at: float


class DeletedCompanyEmployee(BaseModel):
    id: int


class CreateCompany(BaseModel):
    name: str
    overview: str | None = None
    locations: list[CreateCompanyLocation] | None = None
    links: list[CreateCompanyLink] | None = None
    jobs: list | None = None


class CreatedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: list[CreatedCompanyEmployee] | None = None
    locations: list[CreatedCompanyLocation] | None = None
    links: list[CreatedCompanyLink] | None = None
    created_at: float
    updated_at: float


class RetrievedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: list[RetrievedCompanyEmployee] | None = None
    locations: list[CompanyLocation] | None = None
    links: list[RetrievedCompanyLink] | None = None
    created_at: float
    updated_at: float


class RetrievedCurrentCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    locations: list[RetrievedCompanyLocation] | None = None
    links: list[RetrievedCompanyLink] | None = None
    created_at: float
    updated_at: float


class CompanyQueryParameters(BaseModel):
    offset: int | None = None
    limit: int | None = None
    name: str | None = None


class UpdateCompany(BaseModel):
    name: str | None = None
    overview: str | None = None


class UpdatedCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    employees: list[CompanyEmployee] | None = None
    locations: list[CompanyLocation] | None = None
    links: list[CompanyLink] | None = None
    created_at: float
    updated_at: float


class UpdateCurrentCompany(BaseModel):
    name: str | None = None
    overview: str | None = None
    employees: list[UpdateCompanyEmployee] | None = None
    locations: list[UpdateCompanyLocation] | None = None
    links: list[UpdateCompanyLink] | None = None


class UpdatedCurrentCompany(BaseModel):
    id: int
    name: str
    overview: str | None = None
    created_at: float
    updated_at: float


class DeletedCompany(SQLModel):
    id: int


class DeletedCurrentCompany(SQLModel):
    id: int


class EmployeeInvitation(SQLModel):
    title: str
    email: str


class InvitationAcceptance(SQLModel):
    token: str
