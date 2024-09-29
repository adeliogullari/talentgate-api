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
from src.talentgate.auth.crypto.token import BearerToken
from config import Settings, get_settings

InvalidAccessTokenException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="The access token is invalid or has expired",
)

InvalidAuthorizationException = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail="Required permissions are missing to access this resource",
)

InvalidVerificationException = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Invalid verification"
)

InvalidPasswordException = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Invalid password"
)

UserNotFoundByIdException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="The user with the provided id does not exist.",
)

UserNotFoundByEmailException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="The user with the provided email does not exist.",
)

UsernameAlreadyExistsException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="A user with this username already exists"
)

EmailAlreadyExistsException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="A user with this email already exists"
)

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
        raise UserNotFoundByIdException

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
    response_model=CreateUserResponse,
    status_code=201,
    dependencies=[Depends(IsAdminUser)],
)
async def create_user(
    *,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
    user: CreateUserRequest,
) -> User:
    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session, username=user.username
    )

    if retrieved_user:
        raise UsernameAlreadyExistsException

    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=user.email
    )

    if retrieved_user:
        raise EmailAlreadyExistsException

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session, user=user
    )

    return created_user


@router.get(
    path="/api/v1/users/{user_id}",
    response_model=RetrieveUserResponse,
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
        raise UserNotFoundByIdException

    return retrieved_user


@router.get(
    path="/api/v1/users",
    response_model=List[RetrieveUserResponse],
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
    response_model=UpdateUserResponse,
    status_code=200,
    dependencies=[Depends(IsCurrentOrAdminUser)],
)
async def update_user(
    *,
    user_id: int,
    user: UpdateUserRequest,
    sqlmodel_session: Session = Depends(get_sqlmodel_session),
) -> User:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user_id
    )

    if not retrieved_user:
        raise UserNotFoundByIdException

    updated_user = await user_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    return updated_user


@router.delete(
    path="/api/v1/users/{user_id}",
    response_model=DeleteUserResponse,
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
        raise UserNotFoundByIdException

    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    return deleted_user
