from datetime import UTC, datetime, timedelta

from sqlmodel import Field, SQLModel

from config import get_settings
from src.talentgate.database.models import BaseModel

settings = get_settings()


class TokenBlacklist(SQLModel, table=True):
    __tablename__ = "token_blacklist"

    id: int = Field(primary_key=True)
    user_id: int = Field(nullable=False)
    jti: str = Field(unique=True)
    created_at: float | None = Field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    expires_at: float | None = Field(
        default_factory=lambda: (
            datetime.now(UTC) + timedelta(seconds=settings.refresh_token_expiration)
        ).timestamp(),
    )

# class TokenBlacklist(SQLModel, table=True):
#     jti: str = Field(primary_key=True)  # matches the JWT's jti
#     user_id: str = Field(foreign_key="user.id", index=True)
#     revoked_at: datetime = Field(default_factory=datetime.utcnow)
#     reason: Optional[str] = None

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
