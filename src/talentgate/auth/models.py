from datetime import UTC, datetime, timedelta

from sqlmodel import Field, SQLModel

from config import get_settings
from src.talentgate.database.models import BaseModel

settings = get_settings()


class TokenBlacklist(SQLModel, table=True):
    __tablename__ = "token_blacklist"

    id: int = Field(primary_key=True)
    jti: str = Field(unique=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    updated_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC).timestamp()},
    )
    expires_at: float | None = Field(
        default_factory=lambda: (
            datetime.now(UTC) + timedelta(seconds=settings.refresh_token_expiration)
        ).timestamp(),
    )


class BlacklistToken(BaseModel):
    jti: str | None
    user_id: int | None


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


class EmailVerificationQueryParameters(BaseModel):
    token: str | None = None


class ResendEmail(BaseModel):
    email: str


class VerifiedEmail(BaseModel):
    email: str


class RefreshTokens(BaseModel):
    refresh_token: str | None


class LogoutTokens(BaseModel):
    refresh_token: str | None
