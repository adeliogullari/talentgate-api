from sqlmodel import Session
from pytography import JsonWebToken
from typing import List, Sequence, Annotated
from fastapi import Depends, APIRouter, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.talentgate.auth import service as auth_service
from src.talentgate.user import service as user_service
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.user.models import (
    User,
    UserRole,
    CreateUser,
    CreatedUser,
    RetrievedUser,
    RetrievedCurrentUser,
    UserQueryParameters,
    UpdateUser,
    UpdatedUser,
    UpdateCurrentUser,
    UpdatedCurrentUser,
    DeletedUser,
    DeletedCurrentUser,
)
from src.talentgate.auth.exceptions import (
    InvalidAccessTokenException,
    InvalidAuthorizationException,
)
from src.talentgate.user.exceptions import (
    UserIdNotFoundException,
    DuplicateUsernameException,
    DuplicateEmailException,
)
from config import Settings, get_settings

router = APIRouter(tags=["user"])


@router.get(
    path="/api/v1/me",
    response_model=RetrievedCurrentUser,
    status_code=200,
)
async def retrieve_current_user(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    http_authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> User:
    is_verified = auth_service.verify_token(
        token=http_authorization.credentials, key=settings.access_token_key
    )

    if not is_verified:
        raise InvalidAccessTokenException

    _, payload, _ = JsonWebToken.decode(token=http_authorization.credentials)

    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=payload["user_id"]
    )

    if not retrieved_user:
        raise UserIdNotFoundException

    return retrieved_user


class CreateUserDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveUserDependency:
    def __call__(self, user_id: int, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class RetrieveUsersDependency:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class UpdateUserDependency:
    def __call__(self, user_id: int, user: User = Depends(retrieve_current_user)):
        if user.role == UserRole.ADMIN:
            return True
        raise InvalidAuthorizationException


class DeleteUserDependency:
    def __call__(self, user_id: int, user: User = Depends(retrieve_current_user)):
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
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    user: CreateUser,
) -> User:
    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session, username=user.username
    )

    if retrieved_user:
        raise DuplicateUsernameException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=user.email
    )

    if retrieved_user:
        raise DuplicateEmailException

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session, user=user
    )

    return created_user


@router.get(
    path="/api/v1/users/{user_id}",
    response_model=RetrievedUser,
    status_code=200,
    dependencies=[Depends(RetrieveUserDependency())],
)
async def retrieve_user(
    *, user_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise UserIdNotFoundException

    return retrieved_user


@router.get(
    path="/api/v1/users/",
    response_model=List[RetrievedUser],
    status_code=200,
    dependencies=[Depends(RetrieveUsersDependency())],
)
async def retrieve_users(
    *,
    query_parameters: Annotated[UserQueryParameters, Query()],
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> Sequence[User]:
    retrieved_users = await user_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_users


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
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise UserIdNotFoundException

    updated_user = await user_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    return updated_user


@router.patch(
    path="/api/v1/me",
    response_model=UpdatedCurrentUser,
    status_code=200,
)
async def update_current_user(
    *,
    user: UpdateCurrentUser,
    retrieved_user: User = Depends(retrieve_current_user),
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> User:
    updated_user = await user_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    return updated_user


@router.delete(
    path="/api/v1/users/{user_id}",
    response_model=DeletedUser,
    status_code=200,
    dependencies=[Depends(DeleteUserDependency())],
)
async def delete_user(
    *, user_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise UserIdNotFoundException

    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    return deleted_user


@router.delete(
    path="/api/v1/me",
    response_model=DeletedCurrentUser,
    status_code=200,
)
async def delete_current_user(
    *,
    retrieved_user: User = Depends(retrieve_current_user),
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> User:
    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    return deleted_user
