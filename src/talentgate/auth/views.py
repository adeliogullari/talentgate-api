import random
import string
import requests
from sqlmodel import Session
from google.oauth2 import id_token
from fastapi import Depends, APIRouter
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.auth import service as auth_service
from src.talentgate.user import service as user_service
from src.talentgate.user.models import CreateUser
from src.talentgate.user.exceptions import (
    InvalidCredentialsException,
    InvalidVerificationException,
    DuplicateUsernameException,
    DuplicateEmailException,
)
from .models import (
    LoginCredentials,
    LoginTokens,
    GoogleCredentials,
    GoogleTokens,
    LinkedInCredentials,
    LinkedInTokens,
    RegisterCredentials,
    RegisteredUser,
)
from .exceptions import (
    InvalidGoogleIDTokenException,
    InvalidLinkedInAccessTokenException,
)

from config import Settings, get_settings

router = APIRouter(tags=["auth"])


@router.post(path="/api/v1/auth/login", response_model=LoginTokens, status_code=200)
async def login(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: LoginCredentials,
) -> LoginTokens:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=credentials.email
    )

    if not retrieved_user:
        raise InvalidCredentialsException

    if not retrieved_user.verified:
        raise InvalidVerificationException

    if not auth_service.verify_password(
        password=credentials.password, encoded_password=retrieved_user.password
    ):
        raise InvalidCredentialsException

    access_token = auth_service.encode_token(
        user_id=str(retrieved_user.id),
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    refresh_token = auth_service.encode_token(
        user_id=str(retrieved_user.id),
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    return LoginTokens(access_token=access_token, refresh_token=refresh_token)


@router.post(path="/api/v1/auth/google", response_model=GoogleTokens, status_code=200)
async def google(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: GoogleCredentials,
) -> GoogleTokens:
    request = google.auth.transport.requests.Request()

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.token, request=request, audience=settings.google_client_id
    )

    if not id_info:
        raise InvalidGoogleIDTokenException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=id_info["email"]
    )

    email = id_info["email"]

    if not retrieved_user:
        firstname = id_info["given_name"].lower()
        lastname = id_info["family_name"].lower()
        username = f"{firstname}{lastname}{random.randint(1000, 9999)}"
        password = auth_service.encode_password(
            password="".join(random.choices(string.ascii_letters + string.digits, k=16))
        )

        await user_service.create(
            sqlmodel_session=sqlmodel_session,
            user=CreateUser(
                username=username,
                email=email,
                password=password,
                verified=True,
            ),
        )

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=email
    )

    access_token = auth_service.encode_token(
        user_id=str(retrieved_user.id),
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    refresh_token = auth_service.encode_token(
        user_id=str(retrieved_user.id),
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    return GoogleTokens(access_token=access_token, refresh_token=refresh_token)


@router.post(
    path="/api/v1/auth/linkedin", response_model=LinkedInTokens, status_code=200
)
async def linkedin(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: LinkedInCredentials,
) -> LinkedInTokens:
    response = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={
            "Authorization": f"Bearer {credentials.token}",
        },
    )

    if response.status_code != 200:
        raise InvalidLinkedInAccessTokenException

    response_body = response.json()

    email = response_body["emailAddress"]

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=email
    )

    if not retrieved_user:
        firstname = response_body["localizedFirstName"].lower()
        lastname = response_body["localizedLastName"].lower()
        username = f"{firstname}{lastname}{random.randint(1000, 9999)}"
        password = auth_service.encode_password(
            password="".join(random.choices(string.ascii_letters + string.digits, k=16))
        )

        await user_service.create(
            sqlmodel_session=sqlmodel_session,
            user=CreateUser(
                username=username,
                email=email,
                password=password,
                verified=True,
            ),
        )

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=email
    )

    access_token = auth_service.encode_token(
        user_id=str(retrieved_user.id),
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    refresh_token = auth_service.encode_token(
        user_id=str(retrieved_user.id),
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    return LinkedInTokens(access_token=access_token, refresh_token=refresh_token)


@router.post(
    path="/api/v1/auth/register", response_model=RegisteredUser, status_code=200
)
async def register(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    credentials: RegisterCredentials,
) -> RegisteredUser:
    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session, username=credentials.username
    )

    if retrieved_user:
        raise DuplicateUsernameException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=credentials.email
    )

    if retrieved_user:
        raise DuplicateEmailException

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session,
        user=CreateUser(**credentials.model_dump()),
    )

    return created_user
