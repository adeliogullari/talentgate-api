from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

EmailAlreadyVerifiedException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="This email address has already been verified.",
)

InvalidCredentialsException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password.",
)

InvalidVerificationException = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail="Invalid or expired token.",
)

UserIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="No user found with the provided ID.",
)

DuplicateUsernameException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="A user with this username already exists.",
)

DuplicateEmailException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="A user with this email address already exists.",
)
