import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
)


class JwtSchema(BaseModel):
    sub: uuid.UUID
    exp: int
    iat: int
    jti: uuid.UUID
    token_type: str
    iss: str = 'auth-service'

    model_config = ConfigDict(from_attributes=True)


class TokenPairDTO(BaseModel):
    access_token: str
    refresh_token: str
