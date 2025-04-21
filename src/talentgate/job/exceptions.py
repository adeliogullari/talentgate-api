from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

IdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Job not found for the provided id.",
)

ObserverAlreadyExistsException = HTTPException(
    status_code=409,
    detail="Employee is already observing this job.",
)

ObserverNotFoundException = HTTPException(
    status_code=404,
    detail="Given employee is not observing this job.",
)
