import uuid
from typing import Annotated

import jwt
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from auth_service.core.security import decode_access_token

security = HTTPBearer(auto_error=False)


async def get_current_user_id(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> uuid.UUID:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header missing',
        )

    auth_token = credentials.credentials
    try:
        jwt_token = decode_access_token(token=auth_token)
        return jwt_token.sub
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
