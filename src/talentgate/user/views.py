from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from config import Settings, get_settings
from src.talentgate.auth import service as auth_service
from src.talentgate.auth.exceptions import (
    InvalidAccessTokenException,
    InvalidAuthorizationException,
)
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.user import service as user_service
from src.talentgate.user.enums import UserRole
from src.talentgate.user.exceptions import (
    DuplicateEmailException,
    DuplicateUsernameException,
    UserIdNotFoundException,
)
from src.talentgate.user.models import (
    CreatedUser,
    CreateUser,
    DeletedCurrentUser,
    DeletedUser,
    RetrievedCurrentUser,
    RetrievedUser,
    UpdateCurrentUser,
    UpdatedCurrentUser,
    UpdatedUser,
    UpdateUser,
    User,
    UserQueryParameters,
)

router = APIRouter(tags=["users"])


@router.get(
    path="/api/v1/me",
    response_model=RetrievedCurrentUser,
    status_code=200,
)
async def retrieve_current_user(
    *,
    request: Request,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    http_authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
) -> User:
    token = request.cookies.get("access_token") or getattr(
        http_authorization, "credentials", None
    )

    is_verified = auth_service.verify_token(
        token=token,
        key=settings.access_token_key,
    )

    if not is_verified:
        raise InvalidAccessTokenException

    _, payload, _ = auth_service.decode_token(token=token)

    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=payload.get("user_id"),
    )

    if not retrieved_user:
        raise UserIdNotFoundException

    return retrieved_user


class CreateUserDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveUserDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveUsersDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class UpdateUserDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class DeleteUserDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


@router.post(
    path="/api/v1/users",
    response_model=CreatedUser,
    status_code=201,
    dependencies=[Depends(CreateUserDependency())],
)
async def create_user(
    *,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
    user: CreateUser,
) -> User:
    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session,
        username=user.username,
    )

    if retrieved_user:
        raise DuplicateUsernameException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session,
        email=user.email,
    )

    if retrieved_user:
        raise DuplicateEmailException

    return await user_service.create(
        sqlmodel_session=sqlmodel_session,
        user=user,
    )


@router.get(
    path="/api/v1/users/{user_id}",
    response_model=RetrievedUser,
    status_code=200,
    dependencies=[Depends(RetrieveUserDependency())],
)
async def retrieve_user(
    *,
    user_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=user_id,
    )

    if not retrieved_user:
        raise UserIdNotFoundException

    return retrieved_user


@router.get(
    path="/api/v1/users/",
    response_model=list[RetrievedUser],
    status_code=200,
    dependencies=[Depends(RetrieveUsersDependency())],
)
async def retrieve_users(
    *,
    query_parameters: Annotated[UserQueryParameters, Query()],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> Sequence[User]:
    return await user_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session,
        query_parameters=query_parameters,
    )


@router.patch(
    path="/api/v1/users/{user_id}",
    response_model=UpdatedUser,
    status_code=200,
    dependencies=[Depends(UpdateUserDependency())],
)
async def update_user(
    *,
    user_id: int,
    user: UpdateUser,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=user_id,
    )

    if not retrieved_user:
        raise UserIdNotFoundException

    return await user_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
        user=user,
    )


@router.patch(
    path="/api/v1/me",
    response_model=UpdatedCurrentUser,
    status_code=200,
)
async def update_current_user(
    *,
    user: UpdateCurrentUser,
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> User:
    return await user_service.update(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
        user=user,
    )


@router.delete(
    path="/api/v1/users/{user_id}",
    response_model=DeletedUser,
    status_code=200,
    dependencies=[Depends(DeleteUserDependency())],
)
async def delete_user(
    *,
    user_id: int,
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session,
        user_id=user_id,
    )

    if not retrieved_user:
        raise UserIdNotFoundException

    return await user_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
    )


@router.delete(
    path="/api/v1/me",
    response_model=DeletedCurrentUser,
    status_code=200,
)
async def delete_current_user(
    *,
    retrieved_user: Annotated[User, Depends(retrieve_current_user)],
    sqlmodel_session: Annotated[Session, Depends(get_sqlmodel_session)],
) -> User:
    return await user_service.delete(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=retrieved_user,
    )
