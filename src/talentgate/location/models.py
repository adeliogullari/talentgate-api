from sqlmodel import SQLModel


class LoginCredentials(SQLModel):
    email: str
    password: str


class LoginResponse(SQLModel):
    access_token: str | None
    refresh_token: str | None
