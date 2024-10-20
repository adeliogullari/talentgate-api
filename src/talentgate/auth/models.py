from sqlmodel import SQLModel


class LoginCredentials(SQLModel):
    email: str
    password: str


class LoginResponse(SQLModel):
    access_token: str | None
    refresh_token: str | None


class GoogleCredentials(SQLModel):
    token: str | None


class RegisterCredentials(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str


class RegisterResponse(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str


class VerifyToken(SQLModel):
    access_token: str


class TokenVerification(SQLModel):
    is_verified: bool
