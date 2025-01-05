import pytest
from datetime import datetime, UTC
from sqlmodel import Session
from src.talentgate.subscription.models import (
    Subscription,
    SubscriptionPlan,
)


@pytest.fixture
def make_subscription(sqlmodel_session: Session):
    def make(
        plan: SubscriptionPlan | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ):
        subscription = Subscription(
            plan=plan or SubscriptionPlan.BASIC,
            start_date=start_date or datetime.now(UTC),
            end_date=end_date or datetime.now(UTC),
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
