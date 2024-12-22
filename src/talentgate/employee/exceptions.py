from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

IdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Employee not found for the provided id.",
)

EmailNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Employee not found for the provided email.",
)

DuplicateUsernameException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="A employee with this username already exists.",
)

DuplicateEmailException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="A employee with this email already exists."
)
