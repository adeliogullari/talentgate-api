import pytest
import secrets
from sqlmodel import Session
from config import Settings, get_settings
from src.talentgate.user import service as user_service
from src.talentgate.user.models import User, UserRole, UserSubscription


@pytest.fixture
def make_user(sqlmodel_session: Session):
    def make(
        firstname: str = None,
        lastname: str = None,
        username: str = None,
        email: str = None,
        password: str = None,
        verified: bool = None,
        image: str = None,
        role: str = None,
        subscription: str = None,
    ):
        user = User(
            firstname=firstname or "firstname",
            lastname=lastname or "lastname",
            username=username or secrets.token_hex(12),
            email=email or f"{secrets.token_hex(12)}@example.com",
            password=password or user_service.encode_password(password="password"),
            verified=verified or True,
            image=image or "image",
            role=role or UserRole.ACCOUNT_OWNER,
            subscription=subscription or UserSubscription.BASIC,
        )

        sqlmodel_session.add(user)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(user)

        return user

    return make


@pytest.fixture
def user(make_user, request):
    user_params = getattr(request, "param", {})
    firstname = user_params.get("firstname", None)
    lastname = user_params.get("lastname", None)
    username = user_params.get("username", None)
    email = user_params.get("email", None)
    password = user_params.get("password", None)
    verified = user_params.get("verified", None)
    image = user_params.get("image", None)
    role = user_params.get("role", None)
    subscription = user_params.get("subscription", None)

    return make_user(
        firstname=firstname,
        lastname=lastname,
        username=username,
        email=email,
        password=password,
        verified=verified,
        image=image,
        role=role,
        subscription=subscription,
    )
