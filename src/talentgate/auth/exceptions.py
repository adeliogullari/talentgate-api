from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

InvalidAccessTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The access token is invalid or has expired.",
)

InvalidRefreshTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The refresh token is invalid or has expired.",
)

InvalidGoogleIDTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The google id token is invalid or has expired",
)

InvalidLinkedInAccessTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The linkedin access token is invalid or has expired",
)
