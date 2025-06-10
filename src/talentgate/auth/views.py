import random
import string
from typing import Annotated

import requests
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from google.oauth2 import id_token
from sqlmodel import Session
from starlette.status import (
    HTTP_200_OK,
)

from config import Settings, get_settings
from src.talentgate.auth import service as auth_service
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.user import service as user_service
from src.talentgate.user.exceptions import (
    DuplicateEmailException,
    DuplicateUsernameException,
    InvalidCredentialsException,
    InvalidVerificationException,
)
from src.talentgate.user.models import CreateUser, User
from src.talentgate.user.views import retrieve_current_user

from src.talentgate.email.client import EmailClient, get_email_client
from src.talentgate.email import service as email_service
from .exceptions import (
    InvalidGoogleIDTokenException,
    InvalidLinkedInAccessTokenException,
)
from .models import (
    AuthenticationTokens,
    GoogleCredentials,
    GoogleTokens,
    LinkedInCredentials,
    LinkedInTokens,
    LoginCredentials,
    LoginTokens,
    RegisterCredentials,
)

router = APIRouter(tags=["auth"])


@router.post(path="/api/v1/auth/login", status_code=200)
async def login(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    credentials: LoginCredentials,
) -> JSONResponse:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=credentials.email,
    )

    if not retrieved_user:
        raise InvalidCredentialsException

    if not retrieved_user.verified:
        raise InvalidVerificationException

    if not auth_service.verify_password(
        password=credentials.password,
        encoded_password=retrieved_user.password,
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

    content = LoginTokens(access_token=access_token, refresh_token=refresh_token)
    response = JSONResponse(content=content)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    return response


@router.post(path="/api/v1/auth/google", status_code=200)
async def google(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    credentials: GoogleCredentials,
) -> JSONResponse:
    request = google.auth.transport.requests.Request()

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.token,
        request=request,
        audience=settings.google_client_id,
    )

    if not id_info:
        raise InvalidGoogleIDTokenException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=id_info["email"],
    )

    email = id_info["email"]

    if not retrieved_user:
        firstname = id_info["given_name"].lower()
        lastname = id_info["family_name"].lower()
        username = f"{firstname}{lastname}{random.randint(1000, 9999)}"
        password = auth_service.encode_password(
            password="".join(
                random.choices(string.ascii_letters + string.digits, k=16),
            ),
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
        sqlmodel_session=sqlmodel_session,
        email=email,
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

    content = GoogleTokens(access_token=access_token, refresh_token=refresh_token)
    response = JSONResponse(content=content)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    return response


@router.post(
    path="/api/v1/auth/linkedin",
    status_code=200,
)
async def linkedin(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    credentials: LinkedInCredentials,
) -> JSONResponse:
    response = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={
            "Authorization": f"Bearer {credentials.token}",
        },
        timeout=10,
    )

    if response.status_code != HTTP_200_OK:
        raise InvalidLinkedInAccessTokenException

    response_body = response.json()

    email = response_body["emailAddress"]

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=email,
    )

    if not retrieved_user:
        firstname = response_body["localizedFirstName"].lower()
        lastname = response_body["localizedLastName"].lower()
        username = f"{firstname}{lastname}{random.randint(1000, 9999)}"
        password = auth_service.encode_password(
            password="".join(
                random.choices(string.ascii_letters + string.digits, k=16),
            ),
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
        sqlmodel_session=sqlmodel_session,
        email=email,
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

    content = LinkedInTokens(access_token=access_token, refresh_token=refresh_token)
    response = JSONResponse(content=content)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    return response


@router.post(
    path="/api/v1/auth/register",
    status_code=200,
)
async def register(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    email_client: Annotated[EmailClient, Depends(get_email_client)],
    background_tasks: BackgroundTasks,
    credentials: RegisterCredentials,
) -> User:
    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session,
        username=credentials.username,
    )

    if retrieved_user:
        raise DuplicateUsernameException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=credentials.email,
    )

    if retrieved_user:
        raise DuplicateEmailException

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session,
        user=CreateUser(**credentials.model_dump()),
    )

    background_tasks.add_task(
        email_service.send_email,
        email_client,
        "Password Reset",
        "Reset your password",
        "abdullahdeliogullari@outlook.com",
        created_user.email,
    )

    return created_user


@router.post(
    path="/api/v1/auth/token/refresh",
    status_code=200,
)
async def refresh(
    *,
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> JSONResponse:
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token or not auth_service.verify_token(
        token=refresh_token, key=settings.refresh_token_key
    ):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    retrieved_refresh_token = auth_service.retrieve_refresh_token(
        sqlmodel_session=sqlmodel_session,
        refresh_token=refresh_token,
    )

    if retrieved_refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    auth_service.revoke_refresh_token(
        sqlmodel_session=sqlmodel_session,
        retrieved_refresh_token=retrieved_refresh_token,
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

    content = AuthenticationTokens(
        access_token=access_token, refresh_token=refresh_token
    )

    response = JSONResponse(content=content)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    return response


@router.post(
    path="/api/v1/auth/logout",
    status_code=200,
)
async def logout(
    *,
    request: Request,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> JSONResponse:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    retrieved_refresh_token = await auth_service.retrieve_refresh_token(
        sqlmodel_session=sqlmodel_session, refresh_token=refresh_token
    )

    await auth_service.revoke_refresh_token(
        sqlmodel_session=sqlmodel_session,
        retrieved_refresh_token=retrieved_refresh_token,
    )

    content = AuthenticationTokens(
        access_token=access_token, refresh_token=refresh_token
    )

    response = JSONResponse(content=content)

    response.delete_cookie(
        key="access_token", httponly=True, samesite="strict", secure=True
    )

    response.delete_cookie(
        key="refresh_token", httponly=True, samesite="strict", secure=True
    )

    return response
