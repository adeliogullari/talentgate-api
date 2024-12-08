from sqlmodel import SQLModel


class AuthenticationTokens(SQLModel):
    access_token: str | None
    refresh_token: str | None


class LoginCredentials(SQLModel):
    email: str
    password: str


class LoginTokens(AuthenticationTokens):
    pass


class GoogleCredentials(SQLModel):
    token: str | None


class GoogleTokens(AuthenticationTokens):
    pass


class LinkedInCredentials(SQLModel):
    token: str | None


class LinkedInTokens(AuthenticationTokens):
    pass


class RegisterCredentials(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str


class RegisteredUser(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str


class VerifyToken(SQLModel):
    access_token: str


class TokenVerification(SQLModel):
    is_verified: bool


class RefreshToken(SQLModel):
    refresh_token: str


class RefreshedTokens(SQLModel):
    access_token: str
    refresh_token: str
