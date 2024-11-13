import pytest
from config import get_settings
from sqlmodel import Session
from src.talentgate.user.models import User, UserRole, UserSubscription
from src.talentgate.auth.crypto.password.library import PasswordHashLibrary

settings = get_settings()
password_hash_library = PasswordHashLibrary(settings.password_hash_algorithm)


@pytest.fixture
def make_user(sqlmodel_session: Session):
    def make(
        firstname: str = "firstname",
        lastname: str = "lastname",
        username: str = "username",
        email: str = "username@gmail.com",
        password: str = password_hash_library.encode(password="password"),
        verified: bool = True,
        image: str = "image",
        role: str = UserRole.ACCOUNT_OWNER,
        subscription: str = UserSubscription.BASIC
    ):
        user = User(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            password=password,
            verified=verified,
            image=image,
            role=role,
            subscription=subscription
        )

        sqlmodel_session.add(user)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(user)

        return user

    return make


@pytest.fixture
def user(make_user):
    return make_user()
