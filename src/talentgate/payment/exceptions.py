from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
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
