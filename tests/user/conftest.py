import pytest
import secrets
from datetime import datetime, UTC
from sqlmodel import Session
from src.talentgate.user.models import (
    User,
    UserRole,
    UserSubscription,
    SubscriptionType,
)
from src.talentgate.user import service as user_service


@pytest.fixture
def make_user_subscription(sqlmodel_session: Session):
    def make(
        type: SubscriptionType | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ):
        subscription = UserSubscription(
            type=type or SubscriptionType.BASIC,
            start_date=start_date or datetime.now(UTC),
            end_date=end_date or datetime.now(UTC),
        )

        sqlmodel_session.add(subscription)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(subscription)

        return subscription

    return make


@pytest.fixture
def user_subscription(make_user_subscription, request):
    param = getattr(request, "param", {})
    type = param.get("type", None)
    start_date = param.get("start_date", None)
    end_date = param.get("end_date", None)

    return make_user_subscription(
        type=type,
        start_date=start_date,
        end_date=end_date,
    )


@pytest.fixture
def make_user(sqlmodel_session: Session, user_subscription):
    def make(
        firstname: str | None = None,
        lastname: str | None = None,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        verified: bool | None = None,
        role: str = None,
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

    return make_user(
        firstname=firstname,
        lastname=lastname,
        username=username,
        email=email,
        password=password,
        verified=verified,
        role=role,
    )
