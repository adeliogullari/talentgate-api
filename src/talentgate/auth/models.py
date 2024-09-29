from sqlmodel import SQLModel
from datetime import datetime, timedelta
from pydantic import field_validator, Field, ValidationInfo, EmailStr

from config import Settings
from src.talentgate.auth.crypto.password.library import PasswordHashLibrary
from src.talentgate.auth.crypto.token import BearerToken


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
