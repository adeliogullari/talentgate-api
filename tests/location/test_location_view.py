from fastapi.testclient import TestClient


async def test_retrieve_countries(client: TestClient) -> None:
    response = client.get(url=f"/api/v1/location/countries")

    assert response.status_code == 200
    assert "Germany" in response.json()


async def test_retrieve_states_by_country(client: TestClient) -> None:
    response = client.get(url=f"/api/v1/location/countries/Germany/states")

    assert response.status_code == 200
    assert "Bavaria" in response.json()


async def test_retrieve_cities_by_state(client: TestClient) -> None:
    response = client.get(
        url=f"/api/v1/location/countries/Germany/states/Bavaria/cities"
    )

    assert response.status_code == 200
    assert "Munich" in response.json()
