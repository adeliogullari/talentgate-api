from src.talentgate.database.models import BaseModel


class AuthenticationTokens(BaseModel):
    access_token: str | None
    refresh_token: str | None


class LoginCredentials(BaseModel):
    email: str
    password: str


class LoginTokens(AuthenticationTokens):
    pass


class GoogleCredentials(BaseModel):
    token: str | None


class GoogleTokens(AuthenticationTokens):
    pass


class LinkedInCredentials(BaseModel):
    token: str | None


class LinkedInTokens(AuthenticationTokens):
    pass


class RegisterCredentials(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str


class RegisteredUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
