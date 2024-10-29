from typing import List, Sequence

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session
from fastapi import Depends, APIRouter, Query
from src.talentgate.database.service import get_sqlmodel_session
from src.talentgate.user import service as user_service
from src.talentgate.user.models import (
    User,
    UserRole,
    CreateUser,
    CreatedUser,
    RetrievedUser,
    UserQueryParameters,
    UpdateUser,
    UpdatedUser,
    DeletedUser,
)
from src.talentgate.auth.exceptions import (
    InvalidAccessTokenException,
)
from src.talentgate.user.exceptions import (
    IdNotFoundException,
    DuplicateUsernameException,
    DuplicateEmailException,
)
from src.talentgate.auth.crypto.token import BearerToken
from config import Settings, get_settings

router = APIRouter(tags=["user"])


async def retrieve_current_user(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    settings: Settings = Depends(get_settings),
    http_authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> User:
    bearer_token = BearerToken(algorithm=settings.message_digest_algorithm)

    is_verified = bearer_token.verify(
        key=settings.access_token_key, token=http_authorization.credentials
    )

    if not is_verified:
        raise InvalidAccessTokenException

    payload, _, _ = bearer_token.decode(token=http_authorization.credentials)

    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=payload["user_id"]
    )

    if not retrieved_user:
        raise IdNotFoundException

    return retrieved_user


class IsCurrentUser:
    def __call__(self, user_id: int, user: User = Depends(retrieve_current_user)):
        return user.id == user_id


class IsAdminUser:
    def __call__(self, user: User = Depends(retrieve_current_user)):
        return user.role == UserRole.ADMIN


class IsCurrentOrAdminUser:
    def __call__(self, user_id: int, user: User = Depends(retrieve_current_user)):
        return (user.id == user_id) or (user.role == UserRole.ADMIN)


@router.post(
    path="/api/v1/users",
    response_model=CreatedUser,
    status_code=201,
    dependencies=[Depends(IsAdminUser)],
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
    dependencies=[Depends(IsCurrentOrAdminUser)],
)
async def retrieve_user(
    *, user_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise IdNotFoundException

    return retrieved_user


@router.get(
    path="/api/v1/users",
    response_model=List[RetrievedUser],
    status_code=200,
    dependencies=[Depends(IsAdminUser)],
)
async def retrieve_users(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    query_parameters: UserQueryParameters = Query(),
) -> Sequence[User]:
    retrieved_user = await user_service.retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    return retrieved_user


@router.put(
    path="/api/v1/users/{user_id}",
    response_model=UpdatedUser,
    status_code=200,
    dependencies=[Depends(IsCurrentOrAdminUser)],
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
        raise IdNotFoundException

    updated_user = await user_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    return updated_user


@router.delete(
    path="/api/v1/users/{user_id}",
    response_model=DeletedUser,
    status_code=200,
    dependencies=[Depends(IsCurrentOrAdminUser)],
)
async def delete_user(
    *, user_id: int, sqlmodel_session: Session = Depends(get_sqlmodel_session)
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise IdNotFoundException

    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    return deleted_user
