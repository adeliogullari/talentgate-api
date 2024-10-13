import random
import string
from typing import List, Sequence
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime, timedelta, UTC

from sqlmodel import Session
from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.auth import service as auth_service
from src.talentgate.user import service as user_service
from src.talentgate.user.models import (
    User,
    UserRole,
    CreateUserRequest,
    CreateUserResponse,
    RetrieveUserResponse,
    UserQueryParameters,
    UpdateUserRequest,
    UpdateUserResponse,
    DeleteUserResponse,
)
from src.talentgate.user.views import (
    InvalidVerificationException,
    InvalidPasswordException,
    UserNotFoundByEmailException,
    EmailAlreadyExistsException
)
from src.talentgate.auth.models import (
    LoginCredentials,
    LoginResponse,
    GoogleCredentials,
    RegisterCredentials,
    RegisterResponse,
    VerifyToken,
    TokenVerification
)
from src.talentgate.auth.crypto.token import BearerToken
from src.talentgate.auth.crypto.password.library import PasswordHashLibrary
from config import Settings, get_settings

router = APIRouter(tags=["auth"])


@router.post(path="/api/v1/auth/login", response_model=LoginResponse, status_code=200)
async def login(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: LoginCredentials,
) -> LoginResponse:
    bearer_token = BearerToken(algorithm=settings.message_digest_algorithm)
    password_hash_library = PasswordHashLibrary(algorithm=settings.password_hash_algorithm)

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=credentials.email
    )

    if not retrieved_user:
        raise UserNotFoundByEmailException

    if not retrieved_user.verified:
        raise InvalidVerificationException

    if not password_hash_library.verify(
        password=credentials.password, encoded_password=retrieved_user.password
    ):
        raise InvalidPasswordException

    access_token = auth_service.generate_access_token(expiration_minutes=settings.access_token_expiration_minutes,
                                                      user_id=retrieved_user.id,
                                                      algorithm=settings.message_digest_algorithm,
                                                      key=settings.access_token_key)

    refresh_token = auth_service.generate_refresh_token(expiration_days=settings.refresh_token_expiration_days,
                                                        user_id=retrieved_user.id,
                                                        algorithm=settings.message_digest_algorithm,
                                                        key=settings.refresh_token_key)

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post(path="/api/v1/auth/google", response_model=LoginResponse, status_code=200)
async def google(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: GoogleCredentials,
) -> LoginResponse:
    bearer_token = BearerToken(algorithm="scrypt")
    request = requests.Request()

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.token, request=request, audience=settings.google_client_id
    )

    if not id_info:
        raise InvalidVerificationException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=id_info["email"]
    )

    if not retrieved_user:
        await user_service.create(
            sqlmodel_session=sqlmodel_session,
            user=CreateUserRequest(
                username=''.join(random.choices(string.ascii_letters + string.digits, k=12)),
                email=id_info["email"],
                password=''.join(random.choices(string.ascii_letters + string.digits, k=12)),
                verified=True,
            ),
        )

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=id_info["email"]
    )

    access_token = auth_service.generate_access_token(expiration_minutes=settings.access_token_expiration_minutes,
                                                      user_id=retrieved_user.id,
                                                      algorithm=settings.message_digest_algorithm,
                                                      key=settings.access_token_key)

    refresh_token = auth_service.generate_refresh_token(expiration_days=settings.refresh_token_expiration_days,
                                                        user_id=retrieved_user.id,
                                                        algorithm=settings.message_digest_algorithm,
                                                        key=settings.refresh_token_key)

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post(path="/api/v1/auth/linkedin", response_model=LoginResponse, status_code=200)
async def linkedin(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: GoogleCredentials,
) -> LoginResponse:
    bearer_token = BearerToken(algorithm="scrypt")
    request = requests.Request()

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.token, request=request, audience=settings.google_client_id
    )

    if not id_info:
        raise InvalidVerificationException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=id_info["email"]
    )

    if not retrieved_user:
        await user_service.create(
            sqlmodel_session=sqlmodel_session,
            user=CreateUserRequest(
                username=''.join(random.choices(string.ascii_letters + string.digits, k=12)),
                email=id_info["email"],
                password=''.join(random.choices(string.ascii_letters + string.digits, k=12)),
                verified=True,
            ),
        )

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=id_info["email"]
    )

    access_token = auth_service.generate_access_token(expiration_minutes=settings.access_token_expiration_minutes,
                                                      user_id=retrieved_user.id,
                                                      algorithm=settings.message_digest_algorithm,
                                                      key=settings.access_token_key)

    refresh_token = auth_service.generate_refresh_token(expiration_days=settings.refresh_token_expiration_days,
                                                        user_id=retrieved_user.id,
                                                        algorithm=settings.message_digest_algorithm,
                                                        key=settings.refresh_token_key)

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post(
    path="/api/v1/auth/register", response_model=RegisterResponse, status_code=200
)
async def register(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: RegisterCredentials,
) -> User:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=credentials.email
    )

    if retrieved_user:
        raise EmailAlreadyExistsException

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session, user=CreateUserRequest(**credentials.model_dump())
    )

    return created_user


@router.post(
    path="/api/v1/auth/token/verify", response_model=RegisterResponse, status_code=200
)
async def verify_token(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: VerifyToken,
) -> TokenVerification:
    bearer_token = BearerToken(algorithm=settings.message_digest_algorithm)

    is_verified = bearer_token.verify(
        key=settings.access_token_key, token=credentials.access_token
    )

    return TokenVerification(is_verified=is_verified)


@router.post(
    path="/api/v1/auth/token/refresh", response_model=RegisterResponse, status_code=200
)
async def refresh_token(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: RegisterCredentials,
) -> User:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=credentials.email
    )

    if retrieved_user:
        raise EmailAlreadyExistsException

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session, user=CreateUserRequest(**credentials.model_dump())
    )

    return created_user
