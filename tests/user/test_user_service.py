from sqlmodel import Session
from src.talentgate.user.models import (
    User,
    CreateUser,
    UpdateUser,
    UserRole,
    UserSubscription
)
from src.talentgate.user import service as user_service


async def test_verify_password(user: User) -> None:
    is_verified = user_service.verify_password(
        password="password", encoded_password=user.password
    )

    assert is_verified == True


async def test_create(sqlmodel_session: Session) -> None:
    user = CreateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        verified=True,
        image="image",
        role=UserRole.ACCOUNT_OWNER,
        subscription=UserSubscription.BASIC,
    )

    created_user = await user_service.create(
        sqlmodel_session=sqlmodel_session, user=user
    )

    assert created_user.email == user.email


async def test_retrieve_by_id(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user.id
    )

    assert retrieved_user.id == user.id


async def test_retrieve_by_username(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_username(
        sqlmodel_session=sqlmodel_session, username=user.username
    )

    assert retrieved_user.username == user.username


async def test_retrieve_by_email(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await user_service.retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=user.email
    )

    assert retrieved_user.email == user.email


async def test_update(sqlmodel_session: Session, make_user) -> None:
    retrieved_user = make_user()

    user = UpdateUser(
        firstname="firstname",
        lastname="lastname",
        username="username",
        email="username@example.com",
        password="password",
        image="image",
    )

    updated_user = await user_service.update(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    assert user.firstname == updated_user.firstname


async def test_delete(sqlmodel_session, make_user) -> None:
    retrieved_user = make_user()

    deleted_user = await user_service.delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    assert retrieved_user.email == deleted_user.email
