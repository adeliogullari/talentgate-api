from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)

UserSubscriptionNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND, detail="User has no active subscription."
)
