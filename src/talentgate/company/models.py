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


class CompanyLink(SQLModel, table=True):
    __tablename__ = "company_link"

    id: int = Field(primary_key=True)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None, max_length=2048)


class Company(SQLModel, table=True):
    __tablename__ = "company"

    id: int = Field(primary_key=True)
    name: str | None = Field(default=None)
    overview: str | None = Field(default=None)
    locations: CompanyLocationAddress = Relationship(back_populates="company")
    links: CompanyLink = Relationship(back_populates="company")
