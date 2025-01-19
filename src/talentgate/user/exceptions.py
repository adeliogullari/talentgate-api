from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

InvalidCredentialsException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED, detail="Invalid email or password."
)

InvalidVerificationException = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="The user verification is invalid."
)

UserIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="User not found for the provided id.",
)

DuplicateUsernameException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="A user with this username already exists."
)

DuplicateEmailException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="A user with this email already exists."
)
