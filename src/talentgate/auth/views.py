from typing import List, Sequence

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
from src.talentgate.user.views import InvalidVerificationException, InvalidPasswordException, UserNotFoundByEmailException
from models import LoginCredentials, LoginResponse
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
) -> User:
    password_hash_library = PasswordHashLibrary(algorithm=settings.password_hash_algorithm)
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=credentials.email
    )

    if not retrieved_user:
        raise UserNotFoundByEmailException

    if not retrieved_user.verified:
        raise InvalidVerificationException

    if not password_hash_library.verify(password=credentials.password, encoded_password=retrieved_user.password):
        raise InvalidPasswordException

    return retrieved_user


# @router.post(
#     path="/api/v1/auth/register", response_model=RegisterResponse, status_code=200
# )
# async def register(
#     *,
#     sqlmodel_session: Session = Depends(get_sqlmodel_session),
#     settings: Settings = Depends(get_settings),
#     credentials: RegisterCredentials,
# ) -> User | None:
#     retrieved_user = await user_service.retrieve_by_email(
#         sqlmodel_session=sqlmodel_session, user_email=credentials.email
#     )
#
#     if retrieved_user:
#         raise UserEmailAlreadyExistsException
#
#     created_user = await auth_service.register(
#         sqlmodel_session=sqlmodel_session, credentials=credentials
#     )
#
#     if settings.testgate_smtp_email_verification:
#         await aio_kafka_email_producer(
#             value=SendEmail(
#                 subject="Email Verification",
#                 to_addrs=created_user.email,
#                 plain_text_message="Email Verification",
#                 html_message="Email Verification",
#             ).model_dump()
#         )
#
#     return created_user