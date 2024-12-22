import pytest
import secrets
from sqlmodel import Session
from src.talentgate.user.models import User, UserRole, UserSubscription
from src.talentgate.user import service as user_service


@pytest.fixture
def make_user(sqlmodel_session: Session):
    def make(
        firstname: str = None,
        lastname: str = None,
        username: str = None,
        email: str = None,
        password: str = None,
        verified: bool = None,
        role: str = None,
        subscription: str = None,
    ):
        user = User(
            firstname=firstname or secrets.token_hex(12),
            lastname=lastname or secrets.token_hex(12),
            username=username or secrets.token_hex(16),
            email=email or f"{secrets.token_hex(16)}@example.com",
            password=password
            or user_service.encode_password(password=secrets.token_hex(16)),
            verified=verified or True,
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
    param = getattr(request, "param", {})
    firstname = param.get("firstname", None)
    lastname = param.get("lastname", None)
    username = param.get("username", None)
    email = param.get("email", None)
    password = param.get("password", None)
    verified = param.get("verified", None)
    role = param.get("role", None)
    subscription = param.get("subscription", None)

    return make_user(
        firstname=firstname,
        lastname=lastname,
        username=username,
        email=email,
        password=password,
        verified=verified,
        role=role,
        subscription=subscription,
    )
