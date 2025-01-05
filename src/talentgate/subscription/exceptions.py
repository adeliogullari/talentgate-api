from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

IdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Subscription not found for the provided id.",
)
