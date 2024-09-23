from sqlmodel import SQLModel
from datetime import datetime, timedelta
from pydantic import field_validator, Field, ValidationInfo, EmailStr

from config import Settings
from src.talentgate.auth.crypto.password.library import PasswordHashLibrary
from crypto.token import BearerToken

settings = Settings()
password_hash_library = PasswordHashLibrary(
    algorithm=settings.testgate_password_hash_algorithm
)


class LoginCredentials(SQLModel):
    email: str
    password: str


class LoginResponse(SQLModel):
    email: str
    access_token: str | None
    refresh_token: str | None


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
