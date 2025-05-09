import secrets
from datetime import UTC, datetime, timedelta

import pytest
from sqlmodel import Session

from src.talentgate.auth import service as auth_service
from src.talentgate.user.enums import SubscriptionPlan, UserRole
from src.talentgate.user.models import User, UserSubscription


@pytest.fixture
def make_subscription(sqlmodel_session: Session):
    def make(
        plan: str | None = None,
        start_date: float | None = None,
        end_date: float | None = None,
    ):
        subscription = UserSubscription(
            plan=plan or SubscriptionPlan.BASIC.value,
            start_date=start_date
            or (datetime.now(UTC) - timedelta(days=2)).timestamp(),
            end_date=end_date or (datetime.now(UTC) - timedelta(days=1)).timestamp(),
        )

        sqlmodel_session.add(subscription)
        sqlmodel_session.commit()
        sqlmodel_session.refresh(subscription)

        return subscription

    return make


@pytest.fixture
def subscription(make_subscription, request):
    param = getattr(request, "param", {})
    plan = param.get("plan", None)
    start_date = param.get("start_date", None)
    end_date = param.get("end_date", None)

    return make_subscription(
        plan=plan,
        start_date=start_date,
        end_date=end_date,
    )


@pytest.fixture
def make_user(sqlmodel_session: Session, subscription: UserSubscription):
    def make(**kwargs):
        user = User(
            firstname=kwargs.get("firstname") or secrets.token_hex(12),
            lastname=kwargs.get("lastname") or secrets.token_hex(12),
            username=kwargs.get("username") or secrets.token_hex(16),
            email=kwargs.get("email") or f"{secrets.token_hex(16)}@example.com",
            password=kwargs.get("password")
            or auth_service.encode_password(password=secrets.token_hex(16)),
            verified=kwargs.get("verified") or True,
            role=kwargs.get("role") or UserRole.OWNER.value,
            subscription=kwargs.get("subscription") or subscription,
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
