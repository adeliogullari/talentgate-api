import random
import string
from datetime import UTC, datetime, timedelta
from typing import Annotated

import requests
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import JSONResponse
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from paddle_billing import Client
from redis.asyncio import Redis
from sqlmodel import Session
from starlette.status import (
    HTTP_200_OK,
)

from config import Settings, get_settings
from src.talentgate.auth import service as auth_service
from src.talentgate.company import service as company_service
from src.talentgate.company.enums import CompanyEmployeeTitle
from src.talentgate.company.models import CreateCompany, CreateCompanyEmployee
from src.talentgate.database.service import get_redis_client, get_sqlmodel_session
from src.talentgate.email.client import EmailClient, get_email_client
from src.talentgate.payment import service as payment_service
from src.talentgate.payment.service import get_paddle_client
from src.talentgate.user import service as user_service
from src.talentgate.user.enums import UserSubscriptionPlan
from src.talentgate.user.exceptions import (
    DuplicateEmailException,
    DuplicateUsernameException,
    EmailAlreadyVerifiedException,
    InvalidCredentialsException,
    InvalidVerificationException,
)
from src.talentgate.user.models import CreateUser, CreateUserSubscription, UpdateUser, User
from src.talentgate.user.views import retrieve_current_user

from .exceptions import (
    BlacklistedTokenException,
    InvalidGoogleIDTokenException,
    InvalidLinkedInAccessTokenException,
    InvalidRefreshTokenException,
)
from .models import (
    AuthenticationTokens,
    GoogleCredentials,
    LinkedInCredentials,
    LoginCredentials,
    LogoutTokens,
    RefreshTokens,
    RegisterCredentials,
    RegisteredUser,
    ResendCredentials,
    ResendEmail,
    VerifiedEmail,
)

router = APIRouter(tags=["auth"])


@router.post(path="/api/v1/auth/login", status_code=200)
async def login(
    *,
    settings: Annotated[Settings, Depends(get_settings)],
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    background_tasks: BackgroundTasks,
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

    if retrieved_user.subscription.paddle_subscription_id:
        background_tasks.add_task(
            payment_service.sync_subscription,
            paddle_client,
            sqlmodel_session,
            retrieved_user,
        )

    access_token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    refresh_token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    content = AuthenticationTokens(access_token=access_token, refresh_token=refresh_token)

    response = JSONResponse(content=content.model_dump())

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
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
    credentials: GoogleCredentials,
) -> JSONResponse:
    request = google_requests.Request()

    try:
        id_info = id_token.verify_oauth2_token(
            id_token=credentials.token,
            request=request,
            audience=settings.google_client_id,
        )
    except (ValueError, GoogleAuthError) as err:
        raise InvalidGoogleIDTokenException from err

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

        company = await company_service.create(
            sqlmodel_session=sqlmodel_session,
            company=CreateCompany(
                name=f"{username}Company",
            ),
        )

        await company_service.create_employee(
            sqlmodel_session=sqlmodel_session,
            company_id=company.id,
            employee=CreateCompanyEmployee(
                title=CompanyEmployeeTitle.FOUNDER.value,
                user=CreateUser(
                    firstname=firstname,
                    lastname=lastname,
                    username=username,
                    email=email,
                    password=password,
                    verified=True,
                    subscription=CreateUserSubscription(
                        plan=UserSubscriptionPlan.STANDARD.value,
                        start_date=datetime.now(UTC).timestamp(),
                        end_date=(datetime.now(UTC) + timedelta(days=15)).timestamp(),
                    ),
                ),
            ),
        )

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=id_info["email"],
    )

    if retrieved_user.subscription.paddle_subscription_id:
        background_tasks.add_task(
            payment_service.sync_subscription,
            paddle_client,
            sqlmodel_session,
            retrieved_user,
        )

    access_token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    refresh_token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    content = AuthenticationTokens(access_token=access_token, refresh_token=refresh_token)
    response = JSONResponse(content=content.model_dump())

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
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
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

        company = await company_service.create(
            sqlmodel_session=sqlmodel_session,
            company=CreateCompany(
                name=f"{username}Company",
            ),
        )

        await company_service.create_employee(
            sqlmodel_session=sqlmodel_session,
            company_id=company.id,
            employee=CreateCompanyEmployee(
                title=CompanyEmployeeTitle.FOUNDER.value,
                user=CreateUser(
                    firstname=firstname,
                    lastname=lastname,
                    username=username,
                    email=email,
                    password=password,
                    verified=True,
                    subscription=CreateUserSubscription(
                        plan=UserSubscriptionPlan.STANDARD.value,
                        start_date=datetime.now(UTC).timestamp(),
                        end_date=(datetime.now(UTC) + timedelta(days=15)).timestamp(),
                    ),
                ),
            ),
        )

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=email,
    )

    if retrieved_user.subscription.paddle_subscription_id:
        background_tasks.add_task(
            payment_service.sync_subscription,
            paddle_client,
            sqlmodel_session,
            retrieved_user,
        )

    access_token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    refresh_token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    content = AuthenticationTokens(access_token=access_token, refresh_token=refresh_token)
    response = JSONResponse(content=content.model_dump())

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
    response_model=RegisteredUser,
    status_code=201,
)
async def register(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    email_client: Annotated[EmailClient, Depends(get_email_client)],
    settings: Annotated[Settings, Depends(get_settings)],
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

    company = await company_service.create(
        sqlmodel_session=sqlmodel_session,
        company=CreateCompany(
            name=f"{credentials.username}Company",
        ),
    )

    employee = await company_service.create_employee(
        sqlmodel_session=sqlmodel_session,
        company_id=company.id,
        employee=CreateCompanyEmployee(
            title=CompanyEmployeeTitle.FOUNDER.value,
            user=CreateUser(
                **credentials.model_dump(exclude_unset=True, exclude_none=True),
                subscription=CreateUserSubscription(
                    plan=UserSubscriptionPlan.STANDARD.value,
                    start_date=datetime.now(UTC).timestamp(),
                    end_date=(datetime.now(UTC) + timedelta(days=15)).timestamp(),
                ),
            ),
        ),
    )

    token = auth_service.encode_token(
        payload={"user_id": str(employee.user.id)},
        key=settings.one_time_token_key,
        seconds=settings.one_time_token_expiration,
    )

    context = {
        "firstname": employee.user.firstname,
        "link": f"${settings.frontend_base_url}/verify?token={token}",
    }

    await auth_service.send_verification_email(
        email_client=email_client,
        background_tasks=background_tasks,
        context=context,
        from_addr=settings.smtp_email,
        to_addrs=employee.user.email,
    )

    return employee.user


@router.post(
    path="/api/v1/auth/email/verify",
    response_model=VerifiedEmail,
    status_code=200,
)
async def verify_email(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
) -> User:
    if retrieved_user.verified:
        raise EmailAlreadyVerifiedException

    return await user_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
        user=UpdateUser(verified=True),
    )


@router.post(
    path="/api/v1/auth/email/verify/resend",
    response_model=ResendEmail,
    status_code=200,
)
async def resend_verification_email(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    background_tasks: BackgroundTasks,
    settings: Annotated[Settings, Depends(get_settings)],
    email_client: Annotated[EmailClient, Depends(get_email_client)],
    credentials: ResendCredentials,
) -> User:
    retrieved_user = await user_service.retrieve_by_email(sqlmodel_session=sqlmodel_session, email=credentials.email)

    if not retrieved_user:
        raise InvalidCredentialsException

    if retrieved_user.verified:
        raise EmailAlreadyVerifiedException

    token = auth_service.encode_token(
        payload={"user_id": str(retrieved_user.id)},
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    context = {
        "firstname": retrieved_user.firstname,
        "link": f"${settings.frontend_base_url}/verify?token={token}",
    }

    await auth_service.send_verification_email(
        email_client=email_client,
        background_tasks=background_tasks,
        context=context,
        from_addr=settings.smtp_email,
        to_addrs=retrieved_user.email,
    )

    return retrieved_user


@router.post(
    path="/api/v1/auth/token/refresh",
    status_code=200,
)
async def refresh(
    *,
    request: Request,
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    paddle_client: Annotated[Client, Depends(get_paddle_client)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    background_tasks: BackgroundTasks,
    tokens: RefreshTokens,
) -> JSONResponse:
    refresh_token = request.cookies.get("refresh_token") or getattr(tokens, "refresh_token", None)

    if not refresh_token or not auth_service.verify_token(token=refresh_token, key=settings.refresh_token_key):
        raise InvalidRefreshTokenException

    _, payload, _ = auth_service.decode_token(token=refresh_token)

    retrieved_blacklisted_token = await auth_service.retrieve_blacklisted_token(
        redis_client=redis_client,
        jti=payload.get("jti"),
    )

    if retrieved_blacklisted_token:
        raise BlacklistedTokenException

    await auth_service.blacklist_token(
        redis_client=redis_client,
        jti=payload.get("jti"),
        ex=int(settings.refresh_token_expiration),
    )

    access_token = auth_service.encode_token(
        payload={"user_id": str(payload["user_id"])},
        key=settings.access_token_key,
        seconds=settings.access_token_expiration,
    )

    refresh_token = auth_service.encode_token(
        payload={"user_id": str(payload["user_id"])},
        key=settings.refresh_token_key,
        seconds=settings.refresh_token_expiration,
    )

    retrieved_user = await user_service.retrieve_by_id(sqlmodel_session=sqlmodel_session, user_id=payload["user_id"])

    if retrieved_user.subscription.paddle_subscription_id:
        background_tasks.add_task(
            payment_service.sync_subscription,
            paddle_client,
            sqlmodel_session,
            retrieved_user,
        )

    content = AuthenticationTokens(access_token=access_token, refresh_token=refresh_token)

    response = JSONResponse(content=content.model_dump())

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
    settings: Annotated[Settings, Depends(get_settings)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    tokens: LogoutTokens,
) -> JSONResponse:
    refresh_token = request.cookies.get("refresh_token") or getattr(tokens, "refresh_token", None)

    if not refresh_token or not auth_service.verify_token(token=refresh_token, key=settings.refresh_token_key):
        raise InvalidRefreshTokenException

    _, payload, _ = auth_service.decode_token(token=refresh_token)

    retrieved_blacklisted_token = await auth_service.retrieve_blacklisted_token(
        redis_client=redis_client, jti=payload.get("jti")
    )

    if retrieved_blacklisted_token:
        raise BlacklistedTokenException

    await auth_service.blacklist_token(
        redis_client=redis_client,
        jti=payload.get("jti"),
        ex=int(settings.refresh_token_expiration),
    )

    content = AuthenticationTokens(access_token=None, refresh_token=None)

    response = JSONResponse(content=content.model_dump())

    response.delete_cookie(key="access_token", httponly=True, samesite="strict", secure=True)

    response.delete_cookie(key="refresh_token", httponly=True, samesite="strict", secure=True)

    return response
