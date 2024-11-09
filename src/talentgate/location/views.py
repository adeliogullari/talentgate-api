from typing import List
from fastapi import APIRouter
from src.talentgate.location import service as location_service

router = APIRouter(tags=["location"])


@router.get(
    path="/api/v1/location/countries/", response_model=List[str], status_code=200
)
async def retrieve_countries() -> List[str]:
    return location_service.retrieve_countries()


@router.get(
    path="/api/v1/location/countries/{country}/states",
    response_model=List[str],
    status_code=200,
)
async def retrieve_states_by_country(country: str) -> List[str]:
    return location_service.retrieve_states_by_country(country=country)


@router.get(
    path="/api/v1/location/countries/{country}/states/{state}/cities",
    response_model=List[str],
    status_code=200,
)
async def retrieve_cities_by_state(country: str, state: str) -> List[str]:
    return location_service.retrieve_cities_by_state(country=country, state=state)
