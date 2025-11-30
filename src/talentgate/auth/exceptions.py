from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

InvalidAccessTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The access token is invalid or has expired.",
)

InvalidRefreshTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The refresh token is invalid or has expired.",
)

InvalidOneTimeTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The one time token is invalid or has expired.",
)

BlacklistedTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The token has been blacklisted.",
)

InvalidGoogleIDTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The Google ID token is invalid or has expired.",
)

InvalidLinkedInAccessTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="The LinkedIn access token is invalid or has expired.",
)

InvalidAuthorizationException = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail="The required permissions are missing to access this resource.",
)
