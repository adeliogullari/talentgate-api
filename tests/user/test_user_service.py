from sqlmodel import Session
from src.talentgate.user.models import (
    User,
    UserRole,
    CreateUser,
    UpdateUser,
)
from src.talentgate.user.service import (
    create,
    retrieve_by_id,
    retrieve_by_username,
    retrieve_by_email,
    update,
    delete,
)


async def test_create(sqlmodel_session: Session) -> None:
    user = CreateUser(
        username="username", email="username@gmail.com", password="password"
    )

    created_user = await create(sqlmodel_session=sqlmodel_session, user=user)

    assert created_user.email == user.email


async def test_retrieve_by_id(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user.id
    )

    assert retrieved_user.id == user.id


async def test_retrieve_by_username(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await retrieve_by_username(
        sqlmodel_session=sqlmodel_session, username=user.username
    )

    assert retrieved_user.username == user.username


async def test_retrieve_by_email(sqlmodel_session: Session, user: User) -> None:
    retrieved_user = await retrieve_by_email(
        sqlmodel_session=sqlmodel_session, email=user.email
    )

    assert retrieved_user.email == user.email


async def test_update(sqlmodel_session: Session, make_user) -> None:
    retrieved_user = make_user()

    user = UpdateUser(
        firstname="new_firstname",
        lastname="new_lastname",
        username="new_username",
        email="new_username@gmail.com",
        password="new_password",
        verified=True,
        role=UserRole.ADMIN,
        image="new_image",
    )

    updated_user = await update(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user, user=user
    )

    assert user.firstname == updated_user.firstname


async def test_delete(sqlmodel_session, make_user) -> None:
    retrieved_user = make_user()

    deleted_user = await delete(
        sqlmodel_session=sqlmodel_session, retrieved_user=retrieved_user
    )

    assert retrieved_user.firstname == deleted_user.firstname
