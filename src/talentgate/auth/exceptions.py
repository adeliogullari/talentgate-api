from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

InvalidAccessTokenException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="The access token is invalid or has expired.",
)

InvalidRefreshTokenException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="The refresh token is invalid or has expired.",
)
