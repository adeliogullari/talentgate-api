from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

IdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Job not found for the provided id.",
)
