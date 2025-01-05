import json
import pytest
from datetime import datetime, UTC, timezone
from src.talentgate.subscription.models import (
    Subscription,
    SubscriptionPlan,
    SubscriptionStatus,
    CreateSubscription,
    UpdateSubscription,
)
from src.talentgate.user.models import UserRole
from starlette.datastructures import Headers
from fastapi.testclient import TestClient


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_create_subscription(client: TestClient, headers: Headers) -> None:
    created_subscription = CreateSubscription(
    plan = SubscriptionPlan.STANDARD,
    start_date = datetime.now(timezone.utc),
    end_date = datetime.now(timezone.utc),
    )

    response = client.post(
        url="/api/v1/subscriptions",
        headers=headers,
        json=json.loads(
            created_subscription.model_dump_json(exclude_unset=True, exclude_none=True)
        ),
    )

    assert response.status_code == 201


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_subscription(client: TestClient, subscription: Subscription, headers: Headers) -> None:
    response = client.get(url=f"/api/v1/subscriptions/{subscription.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == subscription.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_retrieve_subscriptions(client: TestClient, subscription: Subscription, headers: Headers) -> None:
    params = {
        "offset": 0,
        "limit": 100,
        "id": subscription.id,
    }

    response = client.get(url="/api/v1/subscriptions", params=params, headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == subscription.id


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_update_subscription(client: TestClient, subscription: Subscription, headers: Headers) -> None:
    updated_subscription = UpdateSubscription(
        plan=SubscriptionPlan.STANDARD,
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc),
    )

    response = client.patch(
        url=f"/api/v1/subscriptions/{subscription.id}",
        headers=headers,
        json=json.loads(
            updated_subscription.model_dump_json(exclude_none=True, exclude_unset=True)
        ),
    )

    assert response.status_code == 200
    assert response.json()["id"] == subscription.id
    assert response.json()["plan"] == updated_subscription.plan


@pytest.mark.parametrize("user", [{"role": UserRole.ADMIN}], indirect=True)
async def test_delete_subscription(client: TestClient, subscription: Subscription, headers: Headers) -> None:
    response = client.delete(url=f"/api/v1/subscriptions/{subscription.id}", headers=headers)

    assert response.status_code == 200
