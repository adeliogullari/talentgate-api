from fastapi import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

InvalidAuthorizationException = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail="The required permissions are missing to access this resource.",
)

InvalidVerificationException = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail="The user verification is invalid",
)

IncorrectPasswordException = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail="The password provided is incorrect.",
)

IdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Company not found for the provided id.",
)

EmailNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="User not found for the provided email.",
)

DuplicateUsernameException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="A user with this username already exists.",
)

DuplicateEmailException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="A user with this email already exists.",
)
