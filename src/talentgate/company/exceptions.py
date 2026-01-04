from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)

EmployeeIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Employee not found for the provided id.",
)

CompanyIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Company not found for the provided id.",
)

CompanyLogoNotFoundException = HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Company has no logo image.")
