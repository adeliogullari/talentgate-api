from sqlmodel import Session
from src.talentgate.user.models import (
    User,
    UserRole,
    CreateUser,
    UpdateUser,
)
from src.talentgate.user import service as user_service


async def test_create(sqlmodel_session: Session) -> None:
    user = CreateUser(
        username="username", email="username@gmail.com", password="password"
    )

    created_user = await user_service.create(sqlmodel_session=sqlmodel_session, user=user)

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
        firstname="updated_firstname",
        lastname="updated_lastname",
        username="updated_username",
        email="updated_username@gmail.com",
        password="updated_password",
        verified=True,
        role=UserRole.ADMIN,
        image="updated_image",
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
