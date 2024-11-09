from src.talentgate.location.service import (
    retrieve_countries,
    retrieve_states_by_country,
    retrieve_cities_by_state,
)


async def test_retrieve_countries() -> None:
    countries = retrieve_countries()
    assert "Germany" in countries


async def test_retrieve_states_by_country() -> None:
    states = retrieve_states_by_country(country="Germany")
    assert "Bavaria" in states


async def test_retrieve_cities_by_state() -> None:
    cities = retrieve_cities_by_state(country="Germany", state="Bavaria")
    assert "Munich" in cities
