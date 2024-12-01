from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

IdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Observer not found for the provided id.",
)


ObserverAlreadyExistsException = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail="Observer already exists for this job.",
)
