from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

# Application Evaluation Exceptions
EvaluationIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Evaluation not found for the provided id.",
)

DuplicateEvaluationException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="You have already submitted an evaluation for this application."
)

# Applcation Exceptions
ApplicationIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Application not found for the provided id.",
)

DuplicateEmailException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="An applicant with this email already exists."
)

DuplicatePhoneException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="An applicant with this phone number already exists.",
)