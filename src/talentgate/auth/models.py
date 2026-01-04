from config import get_settings
from src.talentgate.database.models import BaseModel
from src.talentgate.user.models import CreatedUserSubscription

settings = get_settings()


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
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    verified: bool
    role: str
    subscription: CreatedUserSubscription


class EmailVerificationQueryParameters(BaseModel):
    token: str | None = None


class ResendCredentials(BaseModel):
    email: str


class ResendEmail(BaseModel):
    email: str


class VerifiedEmail(BaseModel):
    email: str


class RefreshTokens(BaseModel):
    refresh_token: str | None = None


class LogoutTokens(BaseModel):
    refresh_token: str | None = None
