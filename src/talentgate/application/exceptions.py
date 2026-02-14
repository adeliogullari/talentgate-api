from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

ApplicationIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Application not found for the provided id.",
)

DuplicateEmailException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="An applicant with this email already exists.",
)

DuplicatePhoneException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="An applicant with this phone number already exists.",
)

ResumeAlreadyExistsException = HTTPException(status_code=HTTP_409_CONFLICT, detail="Resume already exists.")
