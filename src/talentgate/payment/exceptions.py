from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

IncompleteTransactionException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="Incomplete transaction.",
)

UnauthorizedPaymentException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="Unauthorized payment.",
)

InactiveSubscriptionException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="Inactive subscription.",
)

InvalidProductIdException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="Invalid product id.",
)

CustomerIdNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="No customer id found.",
)
