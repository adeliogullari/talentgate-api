from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)

IdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Employee not found for the provided id.",
)
