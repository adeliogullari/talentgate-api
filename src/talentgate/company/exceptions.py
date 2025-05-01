from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)

CompanyIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Company not found for the provided id.",
)
