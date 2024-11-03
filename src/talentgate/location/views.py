from typing import List
from fastapi import Depends, APIRouter
from src.talentgate.location.enums import Countries

router = APIRouter(tags=["auth"])


# @router.post(path="/api/v1/location/countries/{country}/states", response_model=List[str], status_code=200)
# async def retrieve_states() -> List[str]:
#
#     return Countries.value.
#
#     return LoginResponse(access_token=access_token, refresh_token=refresh_token)